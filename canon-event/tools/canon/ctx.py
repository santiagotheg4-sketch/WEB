"""Núcleo del generador de Canon Event.

Cada módulo de tools/features/*.py define `build(c)` y usa SOLO esta API
para escribir funciones, datos y recursos, y para engancharse al mod
(ticks, clics, ajustes, sonidos, modelos...). Así los módulos no se pisan.

Convenciones (ver docs/ARQUITECTURA.md):
- Las funciones de un módulo viven en canon:<carpeta propia>/...
- Tags de entidades nuevas: dv_<algo>. Toda criatura con rig lleva dv_brain.
- Objetivos de scoreboard nuevos: dv.<nombre> (<= 16 caracteres en total).
"""
import json, os, re, shutil
from collections import defaultdict, OrderedDict

NS = 'canon'


class BuildError(Exception):
    pass


def txt(s):
    """Texto para jugadores: sin comillas ni barras (rompen el JSON dentro de NBT)."""
    if "'" in s or '"' in s or '\\' in s:
        raise BuildError('texto con comillas o barra invertida: ' + s)
    return s


def jt(s, color='white', italic=False, bold=False):
    d = {'text': txt(s), 'color': color}
    if italic:
        d['italic'] = True
    if bold:
        d['bold'] = True
    return json.dumps(d, ensure_ascii=False)


def btn(label, cmd, color='#e8c9a8', hover=None):
    d = {'text': txt(label), 'color': color, 'clickEvent': {'action': 'run_command', 'value': cmd}}
    if hover:
        d['hoverEvent'] = {'action': 'show_text', 'contents': txt(hover)}
    return json.dumps(d, ensure_ascii=False)


class Ctx:
    def __init__(self, out):
        self.out = out
        self.fn_dir = os.path.join(out, 'data', NS, 'functions')
        self.files = OrderedDict()       # ruta función -> texto
        self.owner = {}                  # ruta función -> módulo
        self.module = 'core'
        self.hooks = defaultdict(list)   # nombre -> [líneas]
        self.models = {}                 # cmd -> (modelo, módulo)   (leather_horse_armor)
        self.item_models = defaultdict(dict)  # item base -> {cmd: modelo}
        self.sounds = OrderedDict()
        self.lang = OrderedDict()
        self.configs = []                # (nombre, etiqueta, default)
        self.admin_cmds = []             # (comando, descripción)
        self.objectives = OrderedDict()  # nombre -> criterio
        self.consts = set()
        self.patches = []                # (ruta, fn, módulo)
        self.json_files = OrderedDict()  # ruta relativa a out -> (obj, módulo)
        self.uses = []                   # (id, función)
        self.after = []                  # callbacks finales

    # ------------------------------------------------------------ funciones
    def F(self, path, text, replace=False):
        """Escribe canon:<path>. Error si otro módulo ya la escribió (salvo replace=True)."""
        if path in self.files and not replace and self.owner.get(path) != self.module:
            raise BuildError(f'{self.module}: la función {path} ya la escribió {self.owner[path]}')
        lines = [l.strip() for l in text.strip('\n').split('\n')]
        lines = [l for l in lines if l]
        self.files[path] = '\n'.join(lines) + '\n'
        self.owner[path] = self.module

    def A(self, path, text):
        """Agrega líneas al final de una función ya generada en este build."""
        add = '\n'.join(l.strip() for l in text.strip('\n').split('\n') if l.strip()) + '\n'
        self.files[path] = self.files.get(path, '') + add
        self.owner.setdefault(path, self.module)

    def exists(self, path):
        return path in self.files or os.path.exists(os.path.join(self.fn_dir, path + '.mcfunction'))

    def read_base(self, path):
        p = os.path.join(self.fn_dir, path + '.mcfunction')
        return open(p, encoding='utf-8').read()

    def patch(self, path, fn):
        """Modifica una función que ya existe en el mod base (o generada antes).
        fn recibe el texto y devuelve el texto nuevo. Debe ser idempotente."""
        self.patches.append((path, fn, self.module))

    def json(self, rel, obj):
        """Escribe un JSON en out/<rel> (p.ej. 'data/canon/loot_tables/x.json')."""
        if rel in self.json_files and self.json_files[rel][1] != self.module:
            raise BuildError(f'{self.module}: {rel} ya lo escribió {self.json_files[rel][1]}')
        self.json_files[rel] = (obj, self.module)

    def path(self, rel):
        p = os.path.join(self.out, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        return p

    # ------------------------------------------------------------ ganchos
    def on(self, hook, text):
        """hook: load | tick | second | player | npc | click | attack | frames | die |
        luna_notice | menu_extra"""
        for l in text.strip('\n').split('\n'):
            if l.strip():
                self.hooks[hook].append(l.strip())

    def npc(self, tag, fn):
        """Cada tick, como la entidad con `tag` (y dv_npc2) y en su posición."""
        self.on('npc', f'execute if entity @s[tag={tag}] run function canon:{fn}')

    def click(self, tag, fn):
        """Clic derecho sobre una interaction con `tag` (y dv_npc_click). Corre como la
        interaction, en su posición; el jugador que hizo clic tiene el tag dv_talker."""
        self.on('click', f'execute if entity @s[tag={tag}] at @s run function canon:{fn}')

    def attack(self, tag, fn):
        self.on('attack', f'execute if entity @s[tag={tag}] at @s run function canon:{fn}')

    def brain_click(self, click_tag, brain_type, brain_tag, fn, attack_fn=None):
        """Interaction enlazada (por dv.id) a un rig: el clic corre fn como el rig."""
        self.on('click', f'scoreboard players operation #id dv.tmp = @s dv.id\n'
                f'execute if entity @s[tag={click_tag}] as @e[type={brain_type},tag={brain_tag},distance=..8] '
                f'if score @s dv.id = #id dv.tmp at @s run function canon:{fn}')
        if attack_fn:
            self.on('attack', f'scoreboard players operation #id dv.tmp = @s dv.id\n'
                    f'execute if entity @s[tag={click_tag}] as @e[type={brain_type},tag={brain_tag},distance=..8] '
                    f'if score @s dv.id = #id dv.tmp at @s run function canon:{attack_fn}')

    def frames(self, tag, fn):
        """Elige #frame dv.tmp para rigs con dv_rigx y `tag` (0 = modelo base)."""
        self.on('frames', f'execute if entity @s[tag={tag}] run function canon:{fn}')

    def die(self, tag, fn):
        self.on('die', f'execute if entity @s[tag={tag}] run function canon:{fn}')

    def use_item(self, item_id, fn, base='carrot_on_a_stick', cooldown=False):
        """Clic derecho con un ítem carrot_on_a_stick (o warped_fungus_on_a_stick) con canon:{id:item_id}."""
        self.uses.append((item_id, fn, base, cooldown))

    def config(self, name, label, default=1):
        self.configs.append((name, label, default))

    def admin(self, cmd, desc):
        self.admin_cmds.append((cmd, desc))

    def objective(self, name, criteria='dummy'):
        if len(name) > 16:
            raise BuildError('objetivo demasiado largo (máx 16): ' + name)
        if name in self.objectives and self.objectives[name] != criteria:
            raise BuildError(f'objetivo {name} con criterios distintos')
        self.objectives[name] = criteria

    def const(self, n):
        self.consts.add(int(n))

    def sound(self, event, sounds, subtitle=None, replace=False):
        """Agrega/reemplaza un evento en assets/canon/sounds.json."""
        d = {'sounds': sounds}
        if subtitle:
            d['subtitle'] = subtitle
        if event in self.sounds and not replace:
            raise BuildError(f'{self.module}: sonido {event} repetido')
        self.sounds[event] = (d, replace)

    def text(self, key, value):
        self.lang[key] = value

    # ------------------------------------------------------------ modelos
    def model(self, name, cmd):
        """Modelo canon:modelo/<name> en leather_horse_armor con CustomModelData=cmd."""
        if cmd in self.models and self.models[cmd][0] != name:
            raise BuildError(f'{self.module}: CMD {cmd} ya usado por {self.models[cmd]}')
        self.models[cmd] = (name, self.module)
        return cmd

    def item_model(self, base_item, cmd, model):
        """Override de CustomModelData para un ítem vanilla (p.ej. 'paper', 'iron_pickaxe').
        model: 'canon:item/<nombre>'."""
        cur = self.item_models[base_item].get(cmd)
        if cur and cur != model:
            raise BuildError(f'{self.module}: CMD {cmd} de {base_item} ya usado por {cur}')
        self.item_models[base_item][cmd] = model

    # ------------------------------------------------------------ texto / azar
    def pick(self, path, options):
        """Función que ejecuta UNA de las opciones al azar (1.20.1 no tiene /random)."""
        n = len(options)
        if not 1 <= n <= 12:
            raise BuildError('pick admite 1..12 opciones')
        if n == 1:
            self.F(path, options[0])
            return
        lines = ['scoreboard players set #k dv.tmp 0']
        for i, body in enumerate(options):
            self.F(f'{path}/o{i}', body + '\nscoreboard players set #k dv.tmp 1')
            if i < n - 1:
                lines.append(f'execute if score #k dv.tmp matches 0 if predicate canon:azar/1en{n - i} run function canon:{path}/o{i}')
            else:
                lines.append(f'execute if score #k dv.tmp matches 0 run function canon:{path}/o{i}')
        self.F(path, '\n'.join(lines))

    def pick_many(self, path, options):
        """Como pick pero sin límite: agrupa en sub-picks de hasta 12."""
        if len(options) <= 12:
            return self.pick(path, options)
        groups = [options[i:i + 10] for i in range(0, len(options), 10)]
        subs = []
        for gi, g in enumerate(groups):
            self.pick(f'{path}/g{gi}', g)
            subs.append(f'function canon:{path}/g{gi}')
        # ponderado por tamaño aproximado (grupos casi iguales)
        self.pick(path, subs)


# ------------------------------------------------------------ helpers de texto (módulo)

def bubble(tag, text, color, ticks=80):
    """Muestra `text` en la burbuja (text_display con `tag` y el mismo dv.id) del que ejecuta."""
    return (f"scoreboard players operation #id dv.tmp = @s dv.id\n"
            f"execute as @e[type=text_display,tag={tag}] if score @s dv.id = #id dv.tmp run data merge entity @s "
            f"{{text:'{jt(text, color)}',background:1342177280}}\n"
            f"scoreboard players set @s dv.say {ticks}")


def chat(who, wcolor, text, sel='@a[distance=..20]'):
    return f'tellraw {sel} [{jt(who + ": ", wcolor)},{jt(text, "white", True)}]'


def say(who, wcolor, bcolor, text, ticks=90, sel='@a[distance=..20]', btag='dv_xbubble'):
    """Burbuja + chat. Para rigs con burbuja dv_xbubble (x/add_bubble)."""
    return bubble(btag, text, bcolor, ticks) + '\n' + chat(who, wcolor, text, sel)


def menu(sel, title, tcolor, buttons):
    parts = ['""', jt('\n' + title + '\n', tcolor)]
    for label, cmd in buttons:
        parts.append(btn(' [' + label + '] ', cmd))
    return f'tellraw {sel} [' + ','.join(parts) + ']'


def rig_summon(tags, name, color, head=True, scale=1.0, health=None, invul=True, base='zombie', extra_nbt='',
               ai=False, view=None):
    """Summon de un rig: entidad cerebro invisible + displays (cuerpo y cabeza opcional).
    Tras el summon, llama a la init de tu módulo con:
      execute as @e[type=<base>,tag=dv_new,tag=<tu_tag>,distance=..2,limit=1,sort=nearest] at @s run function ...
    y en la init: function canon:rig/init_common + set_cmd(...)"""
    s = scale
    tb = round(1.375 * s, 4)
    th = round(1.4375 * s, 4)
    vr = view or (1.2 if s <= 1.2 else 2.0)
    part = lambda kind, t: ('{id:"minecraft:item_display",Tags:["dv_part","dv_%s","dv_cal","dv_rot"],item_display:"none",view_range:%sf,'
                            'item:{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7319999}},'
                            'transformation:{translation:[0f,%sf,0f],left_rotation:[0f,0f,0f,1f],scale:[%sf,%sf,%sf],right_rotation:[0f,0f,0f,1f]}}'
                            % (kind, vr, t, s, s, s))
    pas = [part('body', tb)]
    if head:
        pas.append(part('head', th))
    tagl = ','.join('"%s"' % t for t in ['dv_brain', 'dv_npc2', 'dv_rigx', 'dv_new'] + list(tags))
    hp = ''
    if health:
        hp = f',Health:{health}f,Attributes:[{{Name:"minecraft:generic.max_health",Base:{health}d}}]'
    helmet = ''
    if base in ('zombie', 'husk', 'skeleton', 'zombie_villager', 'drowned', 'stray'):
        helmet = (',CanPickUpLoot:0b,ArmorItems:[{},{},{},{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7319999}}],'
                  'ArmorDropChances:[0f,0f,0f,0f],HandDropChances:[0f,0f]')
    baby = ',IsBaby:0b' if base in ('zombie', 'husk', 'zombie_villager', 'drowned') else ''
    noai = '' if ai else ',NoAI:1b'
    return ('summon minecraft:%s ~ ~ ~ {Tags:[%s],CustomName:\'%s\',Silent:1b,PersistenceRequired:1b%s,Invulnerable:%s%s%s,'
            'DeathLootTable:"canon:vacio"%s%s,Passengers:[%s]}'
            % (base, tagl, jt(name, color), noai, '1b' if invul else '0b', baby, helmet, hp, extra_nbt, ','.join(pas)))


def set_cmd(part, cmd):
    """Fija el modelo base de una parte (body|head) del rig que ejecuta."""
    return (f"execute on passengers if entity @s[tag=dv_{part}] run scoreboard players set @s dv.cmd {cmd}\n"
            f"execute on passengers if entity @s[tag=dv_{part},tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value {cmd}")


def head(cmd):
    return set_cmd('head', cmd)


def item_nbt(item_id, name, color, lore=(), cmd=None, extra=''):
    """NBT de un ítem del mod: canon:{id:...}, nombre y lore sin cursiva."""
    parts = []
    if cmd:
        parts.append(f'CustomModelData:{cmd}')
    parts.append(f'canon:{{id:"{item_id}"}}')
    lore_s = ','.join("'" + jt(l, 'gray').replace('}', ',"italic":false}') + "'" for l in lore)
    name_s = jt(name, color).replace('}', ',"italic":false}')
    parts.append(f"display:{{Name:'{name_s}'" + (f',Lore:[{lore_s}]' if lore else '') + '}')
    if extra:
        parts.append(extra)
    return '{' + ','.join(parts) + '}'


def loot_item(base_item, nbt, count=1):
    """Loot table que da un ítem con NBT."""
    fn = [{'function': 'minecraft:set_nbt', 'tag': nbt}]
    if count != 1:
        fn.append({'function': 'minecraft:set_count', 'count': count})
    return {'type': 'minecraft:generic', 'pools': [{'rolls': 1, 'entries': [
        {'type': 'minecraft:item', 'name': 'minecraft:' + base_item, 'functions': fn}]}]}
