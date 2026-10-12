"""Construye Canon Event.

  base/  (mod 2.0.0 original, intacto)  ->  build/out/  (+ módulos de tools/features)
  -> verificación (tools/check.py) -> build/canon-event-<ver>-1.20.1.jar

Uso: python3 tools/build.py [--no-check] [--only modulo1,modulo2] [--no-jar]
"""
import importlib, json, os, shutil, subprocess, sys, zipfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

from canon.ctx import Ctx, BuildError, jt  # noqa: E402
from canon import models as M  # noqa: E402

VERSION = '9.0.0'
FIRST = ['core']          # módulos que corren primero
LAST = ['remodel']        # módulos que corren al final (pueden reemplazar modelos)


def feature_modules(only=None):
    names = sorted(f[:-3] for f in os.listdir(os.path.join(TOOLS, 'features'))
                   if f.endswith('.py') and not f.startswith('_'))
    order = [n for n in FIRST if n in names] + [n for n in names if n not in FIRST + LAST] + [n for n in LAST if n in names]
    if only:
        keep = set(only) | set(FIRST)
        order = [n for n in order if n in keep]
    return order


HANDHELD = ('pickaxe', 'shovel', '_axe', 'sword', '_hoe', 'stick', 'bone', 'blaze_rod')


def item_parent(item):
    if item in ('carrot_on_a_stick', 'warped_fungus_on_a_stick', 'fishing_rod'):
        return 'minecraft:item/handheld_rod'
    if any(k in item for k in HANDHELD):
        return 'minecraft:item/handheld'
    return 'minecraft:item/generated'


def finalize(c):
    out = c.out
    # -------- ganchos -> funciones
    load = ['# generado: objetivos y constantes de los módulos']
    for name, crit in c.objectives.items():
        load.append(f'scoreboard objectives add {name} {crit}')
    for n in sorted(c.consts):
        load.append(f'scoreboard players set #{n} dv.math {n}')
    for name, label, default in c.configs:
        load.append(f'execute unless score #{name} dv.cfg matches 0.. run scoreboard players set #{name} dv.cfg {default}')
    load += c.hooks['load']
    c.F('extra/load', '\n'.join(load), replace=True)
    c.F('extra/tick', '# cada tick (contexto del servidor)\n' + '\n'.join(c.hooks['tick']), replace=True)
    c.F('extra/second', '# una vez por segundo\n' + '\n'.join(c.hooks['second']), replace=True)
    c.F('extra/player', '# cada tick, como cada jugador y en su posición\n' + '\n'.join(c.hooks['player']), replace=True)
    c.F('npc2/tick', '# rigs de los módulos (dv_npc2)\n' + '\n'.join(c.hooks['npc']), replace=True)
    c.F('npc2/clicked', '# clic en interactions dv_npc_click (jugador = dv_talker)\n' + '\n'.join(c.hooks['click']), replace=True)
    c.F('npc2/attacked', '# golpe en interactions dv_npc_click (jugador = dv_talker)\n' + '\n'.join(c.hooks['attack']), replace=True)
    c.F('rig/frames/extra', '# poses de rigs dv_rigx\n' + '\n'.join(c.hooks['frames']), replace=True)
    if c.hooks['die']:
        c.F('rig/die_extra', '\n'.join(c.hooks['die']), replace=True)
        c.patch('rig/die', lambda s: s if 'rig/die_extra' in s else s.rstrip('\n') + '\nfunction canon:rig/die_extra\n')
    if c.hooks['luna_notice']:
        c.F('luna/notice_extra', '\n'.join(c.hooks['luna_notice']), replace=True)
        c.patch('luna/notice', lambda s: s if 'luna/notice_extra' in s else s.rstrip('\n') + '\nfunction canon:luna/notice_extra\n')
    # -------- ajustes
    entries = ''
    for name, label, default in c.configs:
        c.F(f'admin/config/{name}', f'''
execute if score #{name} dv.cfg matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score #{name} dv.cfg matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation #{name} dv.cfg = #tg dv.tmp
function canon:admin/config
''', replace=True)
        entries += (',' + json.dumps({'text': f'[{label}] ', 'color': '#e8c9a8', 'clickEvent': {'action': 'run_command', 'value': f'/function canon:admin/config/{name}'}}, ensure_ascii=False)
                    + ',' + json.dumps({'score': {'name': f'#{name}', 'objective': 'dv.cfg'}, 'color': 'white'}) + ',{"text":"\\n"}')
    if entries:
        c.F('admin/config_extra', 'tellraw @s [""' + entries + ']', replace=True)
        c.patch('admin/config', lambda s: s if 'admin/config_extra' in s else s.rstrip('\n') + '\nfunction canon:admin/config_extra\n')
    # -------- comandos de admin
    if c.admin_cmds:
        parts = ['""', jt('\nCOMANDOS DE CANON EVENT 3\n', '#ffb347')]
        for cmd, desc in c.admin_cmds:
            parts.append(json.dumps({'text': cmd, 'color': '#e8c9a8', 'clickEvent': {'action': 'suggest_command', 'value': cmd}}, ensure_ascii=False))
            parts.append(jt('  ' + desc + '\n', 'dark_gray'))
        c.F('menu/commands2', 'tellraw @s [' + ','.join(parts) + ']', replace=True)
        c.patch('menu/trigger', lambda s: s if 'menu/commands2' in s else s.replace(
            'scoreboard players set @s dv.menu 0',
            'execute if score @s dv.menu matches 5 run function canon:menu/commands2\nscoreboard players set @s dv.menu 0'))
    # -------- ítems de clic derecho
    use_lines = []
    for item_id, fn, base, cooldown in c.uses:
        pred = {'condition': 'minecraft:any_of', 'terms': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'mainhand': {
                'items': ['minecraft:' + base], 'nbt': '{canon:{id:"%s"}}' % item_id}}}},
            {'condition': 'minecraft:all_of', 'terms': [
                {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'offhand': {
                    'items': ['minecraft:' + base], 'nbt': '{canon:{id:"%s"}}' % item_id}}}},
                {'condition': 'minecraft:inverted', 'term': {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                             'predicate': {'equipment': {'mainhand': {'items': ['minecraft:' + base]}}}}}]}]}
        c.json(f'data/canon/predicates/mano/{item_id}.json', pred)
        cd = ' unless score @s dv.cool matches 1..' if cooldown else ''
        if base == 'carrot_on_a_stick':
            use_lines.append(f'execute if predicate canon:mano/{item_id}{cd} run function canon:{fn}')
        else:
            raise BuildError('use_item: solo carrot_on_a_stick por ahora')
    if use_lines:
        c.F('items/use_extra', '\n'.join(use_lines), replace=True)
        c.patch('items/use', lambda s: s if 'items/use_extra' in s else s.rstrip('\n') + '\nfunction canon:items/use_extra\n')
    # -------- escribir funciones
    for path, text in c.files.items():
        p = os.path.join(c.fn_dir, path + '.mcfunction')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
    # -------- parches
    for path, fn, mod in c.patches:
        p = os.path.join(c.fn_dir, path + '.mcfunction')
        if not os.path.exists(p):
            raise BuildError(f'{mod}: parche sobre función inexistente {path}')
        s = open(p, encoding='utf-8').read()
        s2 = fn(s)
        if s2 is None or s2 == '':
            raise BuildError(f'{mod}: parche de {path} devolvió vacío')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(s2)
    # -------- JSON de datos / recursos
    for rel, (obj, mod) in c.json_files.items():
        p = c.path(rel)
        with open(p, 'w', encoding='utf-8') as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=1)
    # -------- sonidos
    sp = os.path.join(out, 'assets', 'canon', 'sounds.json')
    sj = json.load(open(sp, encoding='utf-8'))
    for ev, (d, replace) in c.sounds.items():
        if ev in sj and not replace:
            raise BuildError(f'sonido {ev} ya existe en el mod base (usa replace=True)')
        sj[ev] = d
    json.dump(sj, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # -------- idiomas
    for lf in ('es_es', 'es_mx', 'es_ar', 'en_us'):
        lp = os.path.join(out, 'assets', 'canon', 'lang', lf + '.json')
        lj = json.load(open(lp, encoding='utf-8'))
        lj.update(c.lang)
        json.dump(lj, open(lp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # -------- modelos (leather_horse_armor)
    mp = os.path.join(out, 'assets', 'minecraft', 'models', 'item', 'leather_horse_armor.json')
    mj = json.load(open(mp))
    base = {o['predicate']['custom_model_data']: o['model'] for o in mj['overrides']}
    for cmd, (name, mod) in c.models.items():
        model = 'canon:modelo/' + name
        if cmd in base and base[cmd] != model:
            raise BuildError(f'{mod}: CMD {cmd} ya lo usa el mod base ({base[cmd]})')
        base[cmd] = model
    mj['overrides'] = [{'predicate': {'custom_model_data': k}, 'model': v} for k, v in sorted(base.items())]
    json.dump(mj, open(mp, 'w'), indent=1)
    # -------- modelos de ítems vanilla
    for item, cm in c.item_models.items():
        ip = os.path.join(out, 'assets', 'minecraft', 'models', 'item', item + '.json')
        if os.path.exists(ip):
            ij = json.load(open(ip))
        else:
            ij = {'parent': item_parent(item), 'textures': {'layer0': 'minecraft:item/' + item}, 'overrides': []}
        cur = {o['predicate']['custom_model_data']: o['model'] for o in ij.get('overrides', [])}
        for cmd, model in cm.items():
            if cmd in cur and cur[cmd] != model:
                raise BuildError(f'CMD {cmd} de {item} ya usado en el mod base por {cur[cmd]}')
            cur[cmd] = model
        ij['overrides'] = [{'predicate': {'custom_model_data': k}, 'model': v} for k, v in sorted(cur.items())]
        json.dump(ij, open(ip, 'w'), indent=1)
    for cb in c.after:
        cb()


def set_version(out):
    p = os.path.join(out, 'META-INF', 'mods.toml')
    s = open(p, encoding='utf-8').read()
    import re
    s = re.sub(r'version="[^"]+"', f'version="{VERSION}"', s, count=1)
    open(p, 'w', encoding='utf-8').write(s)
    fp = os.path.join(out, 'fabric.mod.json')
    fj = json.load(open(fp, encoding='utf-8'))
    fj['version'] = VERSION
    json.dump(fj, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def main():
    args = sys.argv[1:]
    only = None
    if '--only' in args:
        only = args[args.index('--only') + 1].split(',')
    out = os.path.join(ROOT, 'build', 'out')
    if os.path.exists(out):
        shutil.rmtree(out)
    shutil.copytree(os.path.join(ROOT, 'base'), out)
    c = Ctx(out)
    M.set_out(out)
    mods = feature_modules(only)
    for name in mods:
        c.module = name
        mod = importlib.import_module('features.' + name)
        mod.build(c)
    c.module = 'build'
    finalize(c)
    set_version(out)
    print(f'módulos: {", ".join(mods)}  |  funciones generadas: {len(c.files)}  |  modelos nuevos: {len(c.models)}')
    if '--no-check' not in args:
        r = subprocess.run([sys.executable, os.path.join(TOOLS, 'check.py'), out])
        if r.returncode != 0:
            print('LA VERIFICACIÓN FALLÓ: no se arma el .jar')
            sys.exit(1)
    if '--no-jar' in args:
        return
    jar = os.path.join(ROOT, 'build', f'canon-event-{VERSION}-1.20.1.jar')
    if os.path.exists(jar):
        os.remove(jar)
    with zipfile.ZipFile(jar, 'w', zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fs in os.walk(out):
            dn.sort()
            for f in sorted(fs):
                full = os.path.join(dp, f)
                z.write(full, os.path.relpath(full, out))
    print('Listo:', jar)


if __name__ == '__main__':
    try:
        main()
    except BuildError as e:
        print('ERROR DE BUILD:', e)
        sys.exit(2)
