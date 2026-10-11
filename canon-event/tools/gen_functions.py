"""Genera la lógica (mcfunction) de la segunda oleada de Canon Event:
Kevin y sus aventuras (fiesta, bosque, catacumbas, los 3 días, Kevin chistoso),
Nicolás y la mina, el Mirón, la casa blanca de los sueños con Juli y los
eventos nuevos del pueblo.

Uso: python3 tools/gen_functions.py
"""
import json, os, random

ROOT = os.path.join(os.path.dirname(__file__), '..', 'src')
FN = os.path.join(ROOT, 'data', 'canon', 'functions')
DATA = os.path.join(ROOT, 'data', 'canon')
FILES = {}


def F(path, text):
    lines = [l.strip() for l in text.strip('\n').split('\n')]
    lines = [l for l in lines if l]
    FILES[path] = '\n'.join(lines) + '\n'


def A(path, text):
    """Agrega líneas a una función ya generada."""
    FILES[path] = FILES.get(path, '') + '\n'.join(l.strip() for l in text.strip('\n').split('\n') if l.strip()) + '\n'


def txt(s):
    assert "'" not in s and '"' not in s and '\\' not in s, s
    return s


def jt(s, color='white', italic=False):
    d = {'text': txt(s), 'color': color}
    if italic:
        d['italic'] = True
    return json.dumps(d, ensure_ascii=False)


# ------------------------------------------------------------ utilidades

def pick(path, options):
    """Elige una opción al azar (sin /random, que no existe en 1.20.1)."""
    n = len(options)
    assert 1 <= n <= 12
    if n == 1:
        F(path, options[0])
        return
    lines = ['scoreboard players set #k dv.tmp 0']
    for i, body in enumerate(options):
        F(f'{path}/o{i}', body + '\nscoreboard players set #k dv.tmp 1')
        if i < n - 1:
            lines.append(f'execute if score #k dv.tmp matches 0 if predicate canon:azar/1en{n - i} run function canon:{path}/o{i}')
        else:
            lines.append(f'execute if score #k dv.tmp matches 0 run function canon:{path}/o{i}')
    F(path, '\n'.join(lines))


def bubble(tag, text, color, ticks=80):
    return (f"scoreboard players operation #id dv.tmp = @s dv.id\n"
            f"execute as @e[type=text_display,tag={tag}] if score @s dv.id = #id dv.tmp run data merge entity @s "
            f"{{text:'{jt(text, color)}',background:1342177280}}\n"
            f"scoreboard players set @s dv.say {ticks}")


def chat(who, wcolor, text, sel='@a[distance=..20]'):
    return f'tellraw {sel} [{jt(who + ": ", wcolor)},{jt(text, "white", True)}]'


def kv_say(text, ticks=90, sel='@a[distance=..20]'):
    return bubble('dv_kbubble', text, '#ffd27a', ticks) + '\n' + chat('Kevin', '#ffb347', text, sel)


def btn(label, cmd, color='#e8c9a8', hover=None):
    d = {'text': txt(label), 'color': color, 'clickEvent': {'action': 'run_command', 'value': cmd}}
    if hover:
        d['hoverEvent'] = {'action': 'show_text', 'contents': txt(hover)}
    return json.dumps(d, ensure_ascii=False)


def menu(sel, title, tcolor, buttons):
    parts = ['""', jt('\n' + title + '\n', tcolor)]
    for i, (label, cmd) in enumerate(buttons):
        parts.append(btn(' [' + label + '] ', cmd))
    return f'tellraw {sel} [' + ','.join(parts) + ']'


def rig_summon(tags, name, color, body_cmd=7319999, head=True, scale=1.0, health=None, invul=True):
    s = scale
    tb = round(1.375 * s, 4)
    th = round(1.4375 * s, 4)
    vr = 1.2 if s <= 1.2 else 2.0
    part = lambda kind, t: ('{id:"minecraft:item_display",Tags:["dv_part","dv_%s","dv_cal","dv_rot"],item_display:"none",view_range:%sf,'
                            'item:{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7319999}},'
                            'transformation:{translation:[0f,%sf,0f],left_rotation:[0f,0f,0f,1f],scale:[%sf,%sf,%sf],right_rotation:[0f,0f,0f,1f]}}'
                            % (kind, vr, t, s, s, s))
    pas = [part('body', tb)]
    if head:
        pas.append(part('head', th))
    tagl = ','.join('"%s"' % t for t in ['dv_brain', 'dv_npc2', 'dv_rigx', 'dv_new'] + tags)
    hp = ''
    if health:
        hp = f',Health:{health}f,Attributes:[{{Name:"minecraft:generic.max_health",Base:{health}d}}]'
    return ('summon minecraft:zombie ~ ~ ~ {Tags:[%s],CustomName:\'%s\',Silent:1b,PersistenceRequired:1b,NoAI:1b,Invulnerable:%s,'
            'CanPickUpLoot:0b,IsBaby:0b,ArmorItems:[{},{},{},{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7319999}}],'
            'ArmorDropChances:[0f,0f,0f,0f],HandDropChances:[0f,0f],DeathLootTable:"canon:vacio"%s,Passengers:[%s]}'
            % (tagl, jt(name, color), '1b' if invul else '0b', hp, ','.join(pas)))


def set_cmd(part, cmd):
    """Fija el modelo base de una parte (cuerpo o cabeza) del rig que ejecuta."""
    return (f"execute on passengers if entity @s[tag=dv_{part}] run scoreboard players set @s dv.cmd {cmd}\n"
            f"execute on passengers if entity @s[tag=dv_{part},tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value {cmd}")


def head(cmd):
    return set_cmd('head', cmd)


# ------------------------------------------------------------ modelos (CMD)
CMD = {}


def register_models():
    names = []
    names += ['kevin_' + n for n in ['idle', 'walk_a', 'walk_b', 'dance_a', 'dance_b', 'laugh', 'offer']]
    names += ['kevin_cabeza_' + n for n in ['neutral', 'risa', 'drogado', 'miedo']]
    names += ['nicolas_' + n for n in ['idle', 'walk_a', 'walk_b', 'reach']]
    names += ['nicolas_cabeza_' + n for n in ['burla', 'odio', 'grito']]
    for i in range(3):
        names += [f'fiestero_{i}_' + n for n in ['dance_a', 'dance_b', 'stare']]
    names += ['miron_idle', 'miron_peek']
    names += ['alto_' + n for n in ['idle', 'walk_a', 'walk_b', 'reach']]
    names += ['masa_idle', 'masa_a', 'masa_b']
    p = os.path.join(ROOT, 'assets', 'minecraft', 'models', 'item', 'leather_horse_armor.json')
    d = json.load(open(p))
    ov = [o for o in d['overrides'] if not o['model'].split('/')[-1] in names]
    last = max(o['predicate']['custom_model_data'] for o in ov)
    n = last + 1
    for nm in names:
        CMD[nm] = n
        ov.append({'predicate': {'custom_model_data': n}, 'model': 'canon:modelo/' + nm})
        n += 1
    ov.sort(key=lambda o: o['predicate']['custom_model_data'])
    d['overrides'] = ov
    json.dump(d, open(p, 'w'), indent=1)


# =================================================================== CARGA / HOOKS

def gen_hooks():
    F('extra/load', '''
scoreboard objectives add dv.kv trigger
scoreboard objectives add dv.jr trigger
scoreboard objectives add dv.mst minecraft.mined:minecraft.stone
scoreboard objectives add dv.mds minecraft.mined:minecraft.deepslate
scoreboard objectives add dv.ncd dummy
scoreboard objectives add dv.kz dummy
scoreboard objectives add dv.sb dummy
scoreboard objectives add dv.jcs dummy
scoreboard objectives add dv.mus dummy
scoreboard objectives add dv.kpcd dummy
execute unless score #miron dv.cfg matches 0.. run scoreboard players set #miron dv.cfg 1
execute unless score #kprog dv.dev matches -999999..999999 run scoreboard players set #kprog dv.dev 0
execute unless score #kdays dv.dev matches -999999..999999 run scoreboard players set #kdays dv.dev 0
execute unless score #kev dv.dev matches -999999..999999 run scoreboard players set #kev dv.dev 0
execute unless score #kt dv.dev matches -999999..999999 run scoreboard players set #kt dv.dev 0
execute unless score #kevcd dv.dev matches -999999..999999 run scoreboard players set #kevcd dv.dev 600
execute unless score #mironcd dv.dev matches -999999..999999 run scoreboard players set #mironcd dv.dev 1200
execute unless score #casa_built dv.build matches 0.. run scoreboard players set #casa_built dv.build 0
execute unless score #cata_built dv.build matches 0.. run scoreboard players set #cata_built dv.build 0
execute unless score #jroom dv.dev matches -999999..999999 run scoreboard players set #jroom dv.dev 0
scoreboard players set #6 dv.math 6
scoreboard players set #7 dv.math 7
scoreboard players set #9 dv.math 9
scoreboard players set #80 dv.math 80
scoreboard players set #140 dv.math 140
scoreboard players set #560 dv.math 560
''')

    F('extra/player', '''
# una vez por tick por jugador
scoreboard players enable @s dv.kv
scoreboard players enable @s dv.jr
execute if score @s dv.kv matches 1.. run function canon:kevin/choice
execute if score @s dv.jr matches 1.. run function canon:casa/choice
execute if score @s dv.mst matches 1.. run function canon:nicolas/mined
execute if score @s dv.mds matches 1.. run function canon:nicolas/mined
execute if score #suenos dv.cfg matches 1 if data entity @s SleepingX run function canon:casa/sleeping
execute if score @s dv.kz matches 1.. unless data entity @s SleepingX run scoreboard players set @s dv.kz 0
execute if predicate canon:en_casa_sueno run function canon:casa/player
execute if score @s dv.sb matches 1.. unless predicate canon:en_casa_sueno run scoreboard players set @s dv.sb 0
scoreboard players remove @s[scores={dv.mus=1..}] dv.mus 1
''')

    F('extra/second', '''
# una vez por segundo
scoreboard players remove @a[scores={dv.ncd=1..}] dv.ncd 1
scoreboard players remove @a[scores={dv.kpcd=1..}] dv.kpcd 1
execute if score #mironcd dv.dev matches 1.. run scoreboard players remove #mironcd dv.dev 1
execute if score #kevcd dv.dev matches 1.. run scoreboard players remove #kevcd dv.dev 1
execute if score #miron dv.cfg matches 1 as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if predicate canon:azar/1en600 run function canon:miron/try
execute if score #miron dv.cfg matches 1 as @a[gamemode=!spectator,predicate=canon:en_pueblo] at @s if predicate canon:azar/1en250 run function canon:miron/try
execute if score #nicolas dv.cfg matches 1 as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if entity @s[y=-64,dy=104] if score @s dv.ncd matches ..0 if predicate canon:azar/1en300 run function canon:nicolas/try
execute unless score #nicolas dv.cfg matches 1 as @e[type=zombie,tag=dv_nicolas] at @s run function canon:rig/despawn
execute if score #kevin dv.cfg matches 1 run function canon:kevin/g/run
execute unless score #kevin dv.cfg matches 1 run function canon:kevin/g/off
execute as @a[gamemode=!spectator,predicate=canon:en_pueblo] at @s if predicate canon:azar/1en100 run function canon:town2/event
execute as @a[tag=dv_kpart] unless score #kev dv.dev matches 1.. run tag @s remove dv_kpart
''')

    F('extra/tick', '''
execute as @e[type=item_display,tag=dv_nface] at @s run function canon:nicolas/face_tick
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/tick
execute if score #casa_built dv.build matches 1 run function canon:casa/build_try
execute if score #cata_built dv.build matches 1 run function canon:kevin/cata/build_try
''')

    F('npc2/tick', '''
# NPCs de la segunda oleada
execute if entity @s[tag=dv_kevin] run function canon:kevin/tick
execute if entity @s[tag=dv_kfake] run function canon:kevin/dias/fake_tick
execute if entity @s[tag=dv_fiestero] run function canon:kevin/fiesta/dancer_tick
execute if entity @s[tag=dv_nicolas] run function canon:nicolas/tick
execute if entity @s[tag=dv_miron] run function canon:miron/tick
execute if entity @s[tag=dv_alto] run function canon:alto/tick
execute if entity @s[tag=dv_masa] run function canon:masa/tick
''')

    F('npc2/clicked', '''
# clic en una interacción de la segunda oleada (el jugador tiene dv_talker)
execute if entity @s[tag=dv_nota] at @s run function canon:kevin/bosque/nota_taken
execute if entity @s[tag=dv_cllave] at @s run function canon:kevin/cata/llave_taken
execute if entity @s[tag=dv_creja] at @s run function canon:kevin/cata/reja_used
execute if entity @s[tag=dv_cfoto] at @s run function canon:casa/foto_taken
scoreboard players operation #id dv.tmp = @s dv.id
execute if entity @s[tag=dv_kev_click] as @e[type=zombie,tag=dv_kevin,distance=..6] if score @s dv.id = #id dv.tmp at @s run function canon:kevin/clicked
''')

    F('npc2/attacked', '''
scoreboard players operation #id dv.tmp = @s dv.id
execute if entity @s[tag=dv_kev_click] as @e[type=zombie,tag=dv_kevin,distance=..6] if score @s dv.id = #id dv.tmp at @s run function canon:kevin/attacked
''')

    F('rig/frames/extra', f'''
# poses de la segunda oleada
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if entity @s[tag=dv_kdance] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 3
execute if entity @s[tag=dv_kdance] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 4
execute if entity @s[tag=dv_klaugh] run scoreboard players set #frame dv.tmp 5
execute if entity @s[tag=dv_koffer] run scoreboard players set #frame dv.tmp 6
execute if entity @s[tag=dv_nreach] run scoreboard players set #frame dv.tmp 3
execute if entity @s[tag=dv_areach] run scoreboard players set #frame dv.tmp 3
execute if entity @s[tag=dv_fiestero] run function canon:rig/frames/fiestero
execute if entity @s[tag=dv_miron,tag=dv_mpeek] run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_masa] run function canon:rig/frames/masa
''')
    F('rig/frames/fiestero', '''
scoreboard players set #frame dv.tmp 0
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #10 dv.math
execute if score #c dv.tmp matches 5..9 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_fstare] run scoreboard players set #frame dv.tmp 2
''')
    F('rig/frames/masa', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #24 dv.math
execute if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 1
execute if score #c dv.tmp matches 18..23 run scoreboard players set #frame dv.tmp 2
''')

    # caminar genérico con tp (como Juli) hacia el jugador marcado dv_wtgt
    F('x/walk', '''
tag @s add dv_xwalk
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.16 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
''')
    F('x/walk_slow', '''
tag @s add dv_xwalk
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.12 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
''')
    F('x/creep', '''
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.07 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
''')
    F('x/face', 'execute facing entity @a[tag=dv_wtgt,limit=1] feet run tp @s ~ ~ ~ ~ 0')
    F('x/bubble_clear', '''
scoreboard players set @s dv.say -1
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_xbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":""}',background:0}
''')
    F('x/links_follow', '''
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=interaction,tag=dv_xclick] if score @s dv.id = #id dv.tmp run tp @s ~ ~ ~
execute as @e[type=text_display,tag=dv_xbubble] if score @s dv.id = #id dv.tmp run tp @s ~ ~2.3 ~
''')
    F('x/add_bubble', '''
summon minecraft:text_display ~ ~2.3 ~ {Tags:["dv_link","dv_xbubble","dv_new_link"],billboard:"center",text:'{"text":""}',background:0,see_through:0b,shadow:1b,view_range:0.5f,line_width:170}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
''')
    # mirada: ¿algún jugador marcado dv_lookers mira a esta entidad? -> #seen
    F('x/seen', '''
scoreboard players set #seen dv.tmp 0
tag @s add dv_lookme
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^4 if entity @e[tag=dv_lookme,distance=..2.6] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^8 if entity @e[tag=dv_lookme,distance=..4] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^14 if entity @e[tag=dv_lookme,distance=..6] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^20 if entity @e[tag=dv_lookme,distance=..8] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^28 if entity @e[tag=dv_lookme,distance=..10] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^38 if entity @e[tag=dv_lookme,distance=..13] run scoreboard players set #seen dv.tmp 1
tag @s remove dv_lookme
''')
    F('x/jumpscare', '''
# como jugador: susto con imagen (si los sustos están activos)
execute if score #susto dv.cfg matches 1 run title @s times 0 9 7
execute if score #susto dv.cfg matches 1 run title @s subtitle ""
execute if score #susto dv.cfg matches 1 run title @s title ["",{"text":"\\ue100","font":"canon:susto","color":"white"}]
function canon:fx/shake_big
''')
    F('x/blackout', '''
title @s times 0 50 20
title @s subtitle ""
title @s title ["",{"text":"\\ue105","font":"canon:susto","color":"white"}]
playsound canon:fx.blackout master @s ~ ~ ~ 1 1
''')


# =================================================================== KEVIN

JOKES = [
    '¿Qué le dice un techo a otro? Techo de menos.',
    '¿Cómo se despiden los químicos? Ácido un placer.',
    'Fui al médico y le dije que me dolía aquí, aquí y aquí. Tenía el dedo roto.',
    '¿Por qué el libro de matemáticas está triste? Porque tiene muchos problemas.',
    'Mi abuela me dijo que viviera cada día como si fuera el último. Me pasé el día llorando y llamando a todos.',
    '¿Qué hace una abeja en el gimnasio? ¡Zum-ba!',
    'Le pregunté a la Devota si quería ser mi amiga. Ahora no me deja dormir. Literal.',
    '¿Sabes cuál es el colmo de un fantasma? Que lo dejen en visto.',
    '¿Qué le dijo el pez a otro pez? Nada.',
    'Mariana me miró una vez. Una. Ya no tengo cejas.',
    'Dicen que en la mina hay un man de negro. Yo digo que es el que vende pan. Nunca está.',
    'Me compré un libro de anti-gravedad. No lo puedo soltar.',
]

KEVIN_HOW = [
    'Bien, bien. Bueno, ayer vi una sombra mirándome desde el techo, pero bien.',
    'Con hambre. Siempre con hambre. ¿Tienes pan?',
    'Tranquilo, parce. Mientras tú estés vivo, yo estoy feliz.',
    'Raro. Desde la fiesta escucho música techno en todas partes.',
    'Mejor que nunca. Bueno, mejor que la semana pasada, que me perdí tres días.',
]


def gen_kevin():
    K = CMD
    body, hd = K['kevin_idle'], K['kevin_cabeza_neutral']
    risa, droga, miedo = K['kevin_cabeza_risa'], K['kevin_cabeza_drogado'], K['kevin_cabeza_miedo']
    F('kevin/summon', rig_summon(['dv_kevin'], 'Kevin', '#ffb347') + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_kevin,distance=..2,limit=1,sort=nearest] at @s run function canon:kevin/init')
    F('kevin/init', f'''
function canon:rig/init_common
{set_cmd('body', body)}
{head(hd)}
scoreboard players set @s dv.mode 0
scoreboard players set @s dv.say -1
scoreboard players set @s dv.timer 600
summon minecraft:interaction ~ ~ ~ {{Tags:["dv_link","dv_click","dv_npc_click","dv_kev_click","dv_xclick","dv_new_link"],width:0.8f,height:1.95f,response:1b}}
function canon:x/add_bubble
''')
    # global
    F('kevin/g/off', '''
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
execute as @e[type=zombie,tag=dv_kfake] at @s run function canon:rig/despawn
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/abort
''')
    F('kevin/g/run', '''
execute if score #kprog dv.dev matches 4 run function canon:kevin/dias/second
execute if score #kevcd dv.dev matches ..0 unless score #kprog dv.dev matches 4 unless score #kev dv.dev matches 1.. unless entity @e[type=zombie,tag=dv_kevin] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:azar/1en40 run function canon:kevin/arrive
''')
    F('kevin/arrive', '''
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-7 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^3 ^ ^-4 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/greet
scoreboard players set #kevcd dv.dev 300
''')
    pick('kevin/greet_any', [kv_say(t, 100) for t in [
        '¡Eyyy! ¿Qué más, parce? Te estaba buscando.',
        '¡Eyyy! Adivina quién volvió. Exacto: el más bacano.',
        '¡Uy, qué susto! Pensé que eras la Devota. Jajaja.',
        '¡Eyy! Vine porque me aburro. ¿Hacemos algo?',
    ]])
    F('kevin/greet', '''
playsound canon:kevin.hey neutral @a[distance=..24] ~ ~1.6 ~ 1 1
execute if score #kprog dv.dev matches 0 run function canon:kevin/first
execute unless score #kprog dv.dev matches 0 run function canon:kevin/greet_any
''')
    F('kevin/first', kv_say('¡Eyyy! Soy Kevin. Tú no me conoces, pero yo a ti sí. Tengo planes. Muchos planes.', 140) + '\n' +
      'tellraw @a[distance=..20] ' + jt('(Haz clic derecho en Kevin para hablar con él. Te contará chistes y te llevará a sus aventuras.)', 'gray', True) + '\n'
      'scoreboard players set #kprog dv.dev 1')

    F('kevin/tick', '''
tag @s add dv_kme
scoreboard players operation #kme dv.tmp = @s dv.id
scoreboard players set #kdup dv.tmp 0
execute as @e[type=zombie,tag=dv_kevin,tag=!dv_kme] if score @s dv.id < #kme dv.tmp run scoreboard players set #kdup dv.tmp 1
tag @s remove dv_kme
execute if score #kdup dv.tmp matches 0 run function canon:kevin/tick2
execute if score #kdup dv.tmp matches 1 run function canon:rig/despawn
''')
    F('kevin/tick2', f'''
function canon:x/links_follow
scoreboard players remove @s[scores={{dv.say=1..}}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players remove @s[scores={{dv.timer2=1..}}] dv.timer2 1
execute if score @s dv.timer2 matches 0 run function canon:kevin/pose_reset
tag @a remove dv_wtgt
tag @a[gamemode=!spectator,distance=..64,limit=1,sort=nearest] add dv_wtgt
execute if score @s dv.mode matches 0 run function canon:kevin/m_follow
execute if score @s dv.mode matches 1 if score #m4 dv.clock matches 0 run function canon:x/face
execute if score @s dv.mode matches 2 if score #m4 dv.clock matches 0 run function canon:x/face
tag @a remove dv_wtgt
execute if score @s dv.mode matches 0 unless entity @a[distance=..72] run function canon:kevin/leave
''')
    F('kevin/pose_reset', f'''
scoreboard players set @s dv.timer2 -1
tag @s remove dv_klaugh
tag @s remove dv_koffer
execute unless score @s dv.mode matches 1 run tag @s remove dv_kdance
{head(hd)}
''')
    F('kevin/m_follow', '''
execute if entity @a[tag=dv_wtgt,distance=4..] run function canon:x/walk
execute if entity @a[tag=dv_wtgt,distance=26..] at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-3 run function canon:kevin/catch_up
execute if entity @a[tag=dv_wtgt,distance=..4] if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players remove @s dv.timer 1
execute if score #kprog dv.dev matches 5 run scoreboard players remove @s dv.timer 1
execute if score @s dv.timer matches ..0 if score @s dv.say matches ..0 run function canon:kevin/joke_auto
''')
    F('kevin/catch_up', '''
scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 as @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] at @e[type=marker,tag=dv_spot,limit=1] run tp @s ~ ~ ~
kill @e[type=marker,tag=dv_spot]
''')
    F('kevin/leave', '''
particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.02 12 normal
scoreboard players set #kevcd dv.dev 900
function canon:rig/despawn
''')
    F('kevin/laugh', f'''
playsound canon:kevin.laugh neutral @a[distance=..20] ~ ~1.6 ~ 1 1
tag @s add dv_klaugh
scoreboard players set @s dv.timer2 40
{head(risa)}
''')
    pick('kevin/joke', [kv_say(j, 140, '@a[distance=..20]') + '\nfunction canon:kevin/laugh' for j in JOKES])
    F('kevin/joke_auto', '''
scoreboard players set @s dv.timer 1200
function canon:kevin/joke
''')
    pick('kevin/how', [kv_say(t, 120) for t in KEVIN_HOW])

    F('kevin/clicked', f'''
execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound canon:kevin.hey neutral @a[distance=..12] ~ ~1.6 ~ 0.6 1.1
execute if score #kev dv.dev matches 1 run function canon:kevin/fiesta/clicked
execute if score #kev dv.dev matches 3 run {'function canon:kevin/cata/clicked'}
execute unless score #kev dv.dev matches 1.. run {menu('@a[tag=dv_talker]', 'KEVIN', '#ffb347', [
        ('Cuéntame un chiste', '/trigger dv.kv set 1'),
        ('¿Qué hacemos hoy?', '/trigger dv.kv set 2'),
        ('¿Cómo estás?', '/trigger dv.kv set 3'),
        ('Baila', '/trigger dv.kv set 4'),
        ('¿Tienes algo para mí?', '/trigger dv.kv set 6'),
        ('Chao', '/trigger dv.kv set 5')])}
''')
    F('kevin/attacked', kv_say('¡Ey, ey, tranquilo! Soy yo, Kevin. El bueno.', 80) + '\nfunction canon:kevin/laugh')

    # elecciones (se ejecuta como jugador)
    F('kevin/choice', '''
tag @s add dv_ktalk
scoreboard players set #kc dv.tmp 0
scoreboard players operation #kc dv.tmp = @s dv.kv
scoreboard players set @s dv.kv 0
scoreboard players set #kfound dv.tmp 0
execute as @e[type=zombie,tag=dv_kevin,distance=..16,limit=1,sort=nearest] run scoreboard players set #kfound dv.tmp 1
execute if score #kc dv.tmp matches 21..22 run function canon:kevin/fiesta/drink_choice
execute if score #kfound dv.tmp matches 0 unless score #kc dv.tmp matches 21..22 run tellraw @s {"text":"Kevin no está cerca.","color":"gray","italic":true}
execute if score #kfound dv.tmp matches 1 unless score #kc dv.tmp matches 21..22 as @e[type=zombie,tag=dv_kevin,distance=..16,limit=1,sort=nearest] at @s run function canon:kevin/c/run
tag @s remove dv_ktalk
''')
    F('kevin/c/run', '''
execute if score #kc dv.tmp matches 1 run function canon:kevin/joke
execute if score #kc dv.tmp matches 2 run function canon:kevin/c/plan
execute if score #kc dv.tmp matches 3 run function canon:kevin/how
execute if score #kc dv.tmp matches 4 run function canon:kevin/c/dance
execute if score #kc dv.tmp matches 5 run function canon:kevin/c/bye
execute if score #kc dv.tmp matches 6 run function canon:kevin/c/gift
execute if score #kc dv.tmp matches 11 run function canon:kevin/fiesta/try
execute if score #kc dv.tmp matches 12 run function canon:kevin/bosque/try
execute if score #kc dv.tmp matches 13 run function canon:kevin/cata/try
''')
    plan_menu = lambda sel, title, b: menu(sel, title, '#ffb347', b)
    F('kevin/c/plan', f'''
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
execute unless score #kev dv.dev matches 1.. if score #kprog dv.dev matches 1 run function canon:kevin/c/plan1
execute unless score #kev dv.dev matches 1.. if score #kprog dv.dev matches 2 run function canon:kevin/c/plan2
execute unless score #kev dv.dev matches 1.. if score #kprog dv.dev matches 3 run function canon:kevin/c/plan3
execute unless score #kev dv.dev matches 1.. if score #kprog dv.dev matches 5.. run function canon:kevin/c/plan5
''')
    F('kevin/c/plan1', kv_say('Esta noche hay una fiesta techno. La mejor del mundo. Bueno, la única. ¿Vienes?', 140) + '\n' +
      plan_menu('@a[tag=dv_ktalk]', 'FIESTA TECHNO (de noche)', [('¡Vamos!', '/trigger dv.kv set 11'), ('Ahora no', '/trigger dv.kv set 5')]))
    F('kevin/c/plan2', kv_say('Quiero grabar un video en el bosque. Dicen que ahí vive un man altísimo, sin cara. Ideal para mi canal.', 160) + '\n' +
      plan_menu('@a[tag=dv_ktalk]', 'EL BOSQUE (de noche, en un bosque)', [('Vamos', '/trigger dv.kv set 12'), ('Ni loco', '/trigger dv.kv set 5')]))
    F('kevin/c/plan3', kv_say('Encontré una entrada a unas catacumbas. Huele a muerto. ¿Bajamos?', 140) + '\n' +
      plan_menu('@a[tag=dv_ktalk]', 'LAS CATACUMBAS', [('Bajemos', '/trigger dv.kv set 13'), ('Otro día', '/trigger dv.kv set 5')]))
    F('kevin/c/plan5', kv_say('Ya hicimos de todo... pero yo me lo gozo otra vez. Escoge.', 120) + '\n' +
      plan_menu('@a[tag=dv_ktalk]', 'OTRA VEZ', [('Fiesta', '/trigger dv.kv set 11'), ('Bosque', '/trigger dv.kv set 12'),
                                              ('Catacumbas', '/trigger dv.kv set 13'), ('Nada', '/trigger dv.kv set 5')]))
    F('kevin/c/dance', kv_say('¡Mírame! Paso prohibido número 7.', 100) + '''
tag @s add dv_kdance
scoreboard players set @s dv.timer2 120
function canon:kevin/laugh
scoreboard players set @s dv.timer2 120
''')
    F('kevin/c/bye', kv_say('¡Hágale pues! Nos vemos. Si ves a Mariana, no le digas que me viste.', 60) + '''
scoreboard players set #kevcd dv.dev 1200
scoreboard players set @s dv.mode 9
schedule function canon:kevin/bye_later 60t replace
''')
    F('kevin/bye_later', 'execute as @e[type=zombie,tag=dv_kevin,scores={dv.mode=9}] at @s run function canon:kevin/leave')
    F('kevin/c/gift', '''
execute if entity @a[tag=dv_ktalk,scores={dv.kpcd=1..}] run function canon:kevin/c/gift_no
execute unless entity @a[tag=dv_ktalk,scores={dv.kpcd=1..}] run function canon:kevin/c/gift_yes
''')
    F('kevin/c/gift_no', kv_say('Ya te di algo hoy. No soy un banco, parce.', 80))
    pick('kevin/c/gift_yes', [
        kv_say('Toma, pizza fría. Lo mejor que existe.', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/pizza',
        kv_say('Unas balas que encontré por ahí. No preguntes.', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/balas',
        kv_say('Una linterna. La vas a necesitar más que yo.', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/linterna',
        kv_say('Unos billetes. Los gané en una apuesta con un vagabundo.', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/billete',
        kv_say('Una lata de sopa. Romántico, ¿no?', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/sopa',
    ])
    A('kevin/c/gift_yes', 'scoreboard players set @a[tag=dv_ktalk] dv.kpcd 1200')

    # ---- eventos: dispatcher
    F('kevin/ev/tick', '''
scoreboard players add #kt dv.dev 1
execute if score #kev dv.dev matches 1 run function canon:kevin/fiesta/tick
execute if score #kev dv.dev matches 2 run function canon:kevin/bosque/tick
execute if score #kev dv.dev matches 3 run function canon:kevin/cata/tick
''')
    F('kevin/ev/abort', '''
execute if score #kev dv.dev matches 1 run function canon:kevin/fiesta/cleanup
execute if score #kev dv.dev matches 2 run function canon:kevin/bosque/cleanup
execute if score #kev dv.dev matches 3 run function canon:kevin/cata/cleanup
scoreboard players set #kev dv.dev 0
tag @a remove dv_kpart
''')
    F('kevin/ev/busy', kv_say('Espera, que ya estamos en algo.', 60))


def gen_fiesta():
    K = CMD
    hd, risa, droga = K['kevin_cabeza_neutral'], K['kevin_cabeza_risa'], K['kevin_cabeza_drogado']
    F('kevin/fiesta/try', f'''
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
execute unless score #kev dv.dev matches 1.. if entity @a[tag=dv_ktalk,predicate=canon:de_dia] run function canon:kevin/fiesta/day_no
execute unless score #kev dv.dev matches 1.. if entity @a[tag=dv_ktalk,predicate=canon:de_noche] run function canon:kevin/fiesta/start
''')
    F('kevin/fiesta/day_no', kv_say('La fiesta es de noche, parce. Vuelve a hablarme cuando oscurezca.', 100))
    F('kevin/fiesta/start', '''
scoreboard players set #kev dv.dev 1
scoreboard players set #kt dv.dev 0
scoreboard players set #kdrunk dv.dev 0
tag @a[gamemode=!spectator,distance=..32] add dv_kpart
kill @e[type=marker,tag=dv_fiesta_c]
summon minecraft:marker ~ ~ ~ {Tags:["dv_fiesta_c"]}
scoreboard players set @s dv.mode 1
tag @s add dv_kdance
execute positioned ~3 ~ ~ run function canon:kevin/fiesta/dancer_0
execute positioned ~-3 ~ ~1 run function canon:kevin/fiesta/dancer_1
execute positioned ~1 ~ ~3 run function canon:kevin/fiesta/dancer_2
execute positioned ~-1 ~ ~-3 run function canon:kevin/fiesta/dancer_0
execute positioned ~3 ~ ~-3 run function canon:kevin/fiesta/dancer_1
execute positioned ~-3 ~ ~3 run function canon:kevin/fiesta/dancer_2
execute positioned ~ ~6 ~ run summon minecraft:block_display ~-2 ~ ~ {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:magenta_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~6 ~ run summon minecraft:block_display ~2 ~ ~ {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:cyan_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~6 ~ run summon minecraft:block_display ~ ~ ~2 {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:lime_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~6 ~ run summon minecraft:block_display ~ ~ ~-2 {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:yellow_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
playsound canon:kevin.techno record @a[tag=dv_kpart] ~ ~ ~ 1 1
title @a[tag=dv_kpart] times 10 50 20
title @a[tag=dv_kpart] subtitle {"text":"La mejor fiesta del mundo. La única.","color":"#ffd27a","italic":true}
title @a[tag=dv_kpart] title {"text":"FIESTA TECHNO","color":"#ff5ad1","bold":true}
''' + kv_say('¡EYYY! ¡Bienvenidos a la mejor fiesta del mundo! ¡A bailar!', 120))
    for i in range(3):
        F(f'kevin/fiesta/dancer_{i}', '''
scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/fiesta/dancer_summon_%d
kill @e[type=marker,tag=dv_spot]
''' % i)
        F(f'kevin/fiesta/dancer_summon_{i}', rig_summon(['dv_fiestero'], 'Fiestero', '#c06ad6', head=False) + '\n'
          f'execute as @e[type=zombie,tag=dv_new,tag=dv_fiestero,distance=..2,limit=1,sort=nearest] at @s run function canon:kevin/fiesta/dancer_init_{i}')
        F(f'kevin/fiesta/dancer_init_{i}', f'''
function canon:rig/init_common
{set_cmd('body', K[f'fiestero_{i}_dance_a'])}
scoreboard players set @s dv.anim {i * 3}
execute facing entity @e[type=marker,tag=dv_fiesta_c,limit=1] feet run tp @s ~ ~ ~ ~ 0
''')
    F('kevin/fiesta/dancer_tick', '''
execute unless score #kev dv.dev matches 1 run function canon:rig/despawn
tag @a remove dv_wtgt
execute if entity @s[tag=dv_fstare] run tag @a[tag=dv_kpart,distance=..32,limit=1,sort=nearest] add dv_wtgt
execute if entity @s[tag=dv_fstare] run function canon:x/face
tag @a remove dv_wtgt
''')
    F('kevin/fiesta/tick', '''
execute unless entity @e[type=marker,tag=dv_fiesta_c] run function canon:kevin/fiesta/cleanup
execute unless entity @a[tag=dv_kpart] run function canon:kevin/fiesta/cleanup
execute as @a[tag=dv_kpart] at @s unless entity @e[type=marker,tag=dv_fiesta_c,distance=..48] run tag @s remove dv_kpart
execute if score #kt dv.dev matches ..899 if score #m4 dv.clock matches 0 at @e[type=marker,tag=dv_fiesta_c] run function canon:kevin/fiesta/lights
execute if score #kt dv.dev matches ..899 if score #m20 dv.clock matches 0 run function canon:kevin/fiesta/spin
execute if score #kt dv.dev matches 400 run function canon:kevin/fiesta/offer
execute if score #kt dv.dev matches 520 as @e[type=zombie,tag=dv_kevin] run tag @s remove dv_koffer
execute as @a[tag=dv_kpart,tag=dv_kdrug] at @s if score #m40 dv.clock matches 0 run function canon:kevin/fiesta/trip
execute if score #kt dv.dev matches 900 run function canon:kevin/fiesta/wrong
execute if score #kt dv.dev matches 960 at @e[type=marker,tag=dv_fiesta_c] run function canon:kevin/fiesta/miron
execute if score #kt dv.dev matches 1040 run function canon:kevin/fiesta/scream
execute if score #kt dv.dev matches 1080 run function canon:kevin/fiesta/end
''')
    F('kevin/fiesta/lights', '''
scoreboard players operation #c dv.tmp = #kt dv.dev
scoreboard players operation #c dv.tmp %= #3 dv.math
execute if score #c dv.tmp matches 0 run particle minecraft:dust 1 0.2 0.8 1.6 ~ ~2.5 ~ 4 1.5 4 0 25 force @a[tag=dv_kpart]
execute if score #c dv.tmp matches 1 run particle minecraft:dust 0.2 0.9 1 1.6 ~ ~2.5 ~ 4 1.5 4 0 25 force @a[tag=dv_kpart]
execute if score #c dv.tmp matches 2 run particle minecraft:dust 0.6 1 0.2 1.6 ~ ~2.5 ~ 4 1.5 4 0 25 force @a[tag=dv_kpart]
particle minecraft:end_rod ~ ~6 ~ 2 0.2 2 0.05 3 force @a[tag=dv_kpart]
''')
    F('kevin/fiesta/spin', '''
scoreboard players operation #c dv.tmp = #kt dv.dev
scoreboard players operation #c dv.tmp %= #40 dv.math
execute if score #c dv.tmp matches 0..19 as @e[type=block_display,tag=dv_flight] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{left_rotation:[0f,0.7071f,0f,0.7071f],scale:[1.3f,1.3f,1.3f]}}
execute if score #c dv.tmp matches 20..39 as @e[type=block_display,tag=dv_flight] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
''')
    F('kevin/fiesta/offer', f'''
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/fiesta/offer2
''')
    F('kevin/fiesta/offer2', kv_say('Toma, prueba esto. Te va a encantar. Confía en mí.', 120, '@a[tag=dv_kpart]') + '''
tag @s add dv_koffer
''' + menu('@a[tag=dv_kpart]', 'Kevin te ofrece un vaso con algo brillante...', '#ff5ad1',
           [('Tomar', '/trigger dv.kv set 21'), ('No, gracias', '/trigger dv.kv set 22')]))
    F('kevin/fiesta/clicked', '''
execute if score #kt dv.dev matches ..399 run function canon:kevin/fiesta/talk
execute if score #kt dv.dev matches 400..899 run function canon:kevin/fiesta/offer2
''')
    pick('kevin/fiesta/talk', [kv_say(t, 80, '@a[tag=dv_kpart]') for t in [
        '¡Súbele, súbele! Ah no, no hay volumen. Es mi cabeza.',
        'Este DJ es mi primo. Bueno, no tengo primos. Pero ojalá.',
        '¡Baila conmigo! Nadie nos está mirando. Creo.',
    ]])
    F('kevin/fiesta/drink_choice', '''
execute unless score #kev dv.dev matches 1 run tellraw @s {"text":"Ya no hay nada que tomar.","color":"gray","italic":true}
execute if score #kev dv.dev matches 1 if score #kc dv.tmp matches 21 unless entity @s[tag=dv_kdrug] run function canon:kevin/fiesta/drink
execute if score #kev dv.dev matches 1 if score #kc dv.tmp matches 22 run function canon:kevin/fiesta/refuse
''')
    F('kevin/fiesta/drink', '''
tag @s add dv_kdrug
scoreboard players set #kdrunk dv.dev 1
effect give @s minecraft:nausea 40 0 true
effect give @s minecraft:speed 30 1 true
playsound canon:kevin.drugged music @s ~ ~ ~ 1 1
tellraw @s {"text":"Sabe a chicle y a pilas. Las luces empiezan a respirar.","color":"#ff5ad1","italic":true}
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/laugh
''')
    F('kevin/fiesta/refuse', '''
tellraw @s [{"text":"Kevin: ","color":"#ffb347"},{"text":"Bueno, más para mí. Jajaja.","color":"white","italic":true}]
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/laugh
''')
    F('kevin/fiesta/trip', '''
effect give @s minecraft:darkness 2 0 true
particle minecraft:dust 1 0 1 1 ^ ^1.5 ^2 1 1 1 0 10 normal @s
execute if predicate canon:azar/1en3 run playsound canon:devota.whisper ambient @s ^2 ^ ^-2 0.5 0.6
''')
    F('kevin/fiesta/wrong', f'''
stopsound @a[tag=dv_kpart] record canon:kevin.techno
playsound canon:fx.heartbeat ambient @a[tag=dv_kpart] ~ ~ ~ 1 1
tag @e[type=zombie,tag=dv_fiestero] add dv_fstare
execute as @e[type=block_display,tag=dv_flight] run data merge entity @s {{block_state:{{Name:"minecraft:red_stained_glass"}}}}
execute as @e[type=zombie,tag=dv_kevin,limit=1] run tag @s remove dv_kdance
execute as @e[type=zombie,tag=dv_kevin,limit=1] run {head(droga).splitlines()[0]}
execute as @e[type=zombie,tag=dv_kevin,limit=1] run {head(droga).splitlines()[1]}
tellraw @a[tag=dv_kpart] {{"text":"La música se corta. Todos dejan de bailar. Todos te miran.","color":"#c94a4a","italic":true}}
''')
    F('kevin/fiesta/miron', '''
execute positioned ~2 ~ ~2 run function canon:miron/spawn_here
execute as @e[type=zombie,tag=dv_miron,distance=..8] run scoreboard players set @s dv.timer2 1
playsound canon:miron.aparece hostile @a[tag=dv_kpart] ~ ~ ~ 1 0.9
''')
    F('kevin/fiesta/scream', '''
playsound canon:miron.grito master @a[tag=dv_kpart] ~ ~ ~ 1 1
execute as @a[tag=dv_kpart] at @s run function canon:x/jumpscare
execute as @a[tag=dv_kpart] at @s run function canon:x/blackout
''')
    F('kevin/fiesta/end', f'''
execute if score #kprog dv.dev matches ..1 run scoreboard players set #kprog dv.dev 2
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/fiesta/end_kevin
function canon:kevin/fiesta/cleanup
''')
    F('kevin/fiesta/end_kevin', f'''
scoreboard players set @s dv.mode 0
tag @s remove dv_kdance
execute if score #kdrunk dv.dev matches 1 run function canon:kevin/fiesta/end_drunk
execute if score #kdrunk dv.dev matches 0 run function canon:kevin/fiesta/end_sober
function canon:kevin/laugh
tellraw @a[distance=..40] {jt('(Kevin tiene otra idea. Háblale: ¿Qué hacemos hoy?)', 'gray', True)}
''')
    F('kevin/fiesta/end_drunk', kv_say('Jajaja, ¿qué te pasó? Te quedaste dormido parado. Te dije que te iba a encantar.', 160, '@a[distance=..40]'))
    F('kevin/fiesta/end_sober', kv_say('Bro... ¿viste eso? ¿Quién era ese man flaco? Mejor no volvamos a esa fiesta. O sí. Jajaja.', 160, '@a[distance=..40]'))
    F('kevin/fiesta/cleanup', '''
stopsound @a[tag=dv_kpart] record canon:kevin.techno
stopsound @a[tag=dv_kdrug] music canon:kevin.drugged
execute as @e[type=zombie,tag=dv_fiestero] at @s run function canon:rig/despawn
kill @e[type=block_display,tag=dv_flight]
kill @e[type=marker,tag=dv_fiesta_c]
execute as @e[type=zombie,tag=dv_miron] at @s run function canon:rig/despawn
execute as @e[type=zombie,tag=dv_kevin] run scoreboard players set @s dv.mode 0
execute as @e[type=zombie,tag=dv_kevin] run tag @s remove dv_kdance
tag @a remove dv_kdrug
tag @a remove dv_kpart
scoreboard players set #kev dv.dev 0
''')


NOTAS = ['SIEMPRE MIRA', 'NO CORRAS', 'DETRÁS DE TI', 'KEVIN NO ESTÁ SOLO', 'NO TIENE CARA', 'YA TE VIO']


def gen_bosque():
    F('kevin/bosque/try', f'''
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
scoreboard players set #bok dv.tmp 0
execute if entity @a[tag=dv_ktalk,predicate=canon:de_noche,predicate=canon:en_bosque] run scoreboard players set #bok dv.tmp 1
execute unless score #kev dv.dev matches 1.. if score #bok dv.tmp matches 0 run function canon:kevin/bosque/no
execute unless score #kev dv.dev matches 1.. if score #bok dv.tmp matches 1 at @a[tag=dv_ktalk,limit=1] run function canon:kevin/bosque/start
''')
    F('kevin/bosque/no', kv_say('Tiene que ser de noche y en un bosque de verdad, con árboles. Llévame a uno y me hablas.', 120))
    notes = []
    offs = [(22, 0), (-20, 10), (6, 28), (-8, -26), (26, -18), (-28, -12)]
    for i, (x, z) in enumerate(offs):
        notes.append(f'execute positioned ~{x} ~ ~{z} positioned over motion_blocking_no_leaves run function canon:kevin/bosque/nota_spawn')
    F('kevin/bosque/start', '''
scoreboard players set #kev dv.dev 2
scoreboard players set #kt dv.dev 0
scoreboard players set #knotes dv.dev 0
tag @a[gamemode=!spectator,distance=..32] add dv_kpart
kill @e[type=marker,tag=dv_bosque_c]
summon minecraft:marker ~ ~ ~ {Tags:["dv_bosque_c"]}
''' + '\n'.join(notes) + '''
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:kevin/bosque/kevin_runs
playsound canon:music.bosque music @a[tag=dv_kpart] ~ ~ ~ 1 1
title @a[tag=dv_kpart] times 10 60 20
title @a[tag=dv_kpart] subtitle {"text":"Encuentra las 6 notas. No lo mires mucho tiempo.","color":"gray","italic":true}
title @a[tag=dv_kpart] title {"text":"EL BOSQUE","color":"#d8d8d8"}
''')
    F('kevin/bosque/kevin_runs', kv_say('¡Yo grabo desde allá! ¡Busquen las 6 notas del Alto antes de que los encuentre! Jajaja...', 120, '@a[tag=dv_kpart]') + '''
particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.02 12 normal
function canon:rig/despawn
''')
    F('kevin/bosque/nota_spawn', '''
summon minecraft:item_display ~ ~0.6 ~ {Tags:["dv_nota_vis","dv_bnew"],brightness:{sky:15,block:15},billboard:"vertical",view_range:0.5f,item:{id:"minecraft:paper",Count:1b},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:interaction ~ ~0.1 ~ {Tags:["dv_nota","dv_click","dv_npc_click","dv_bnew"],width:1.0f,height:1.2f,response:1b}
scoreboard players operation @e[tag=dv_bnew] dv.id = #next dv.id
scoreboard players add #next dv.id 1
tag @e[tag=dv_bnew] remove dv_bnew
''')
    F('kevin/bosque/tick', '''
execute unless entity @a[tag=dv_kpart] run function canon:kevin/bosque/fail
execute as @a[tag=dv_kpart] at @s unless entity @e[type=marker,tag=dv_bosque_c,distance=..120] run tag @s remove dv_kpart
execute if score #m40 dv.clock matches 0 as @e[type=item_display,tag=dv_nota_vis] at @s run particle minecraft:end_rod ~ ~0.4 ~ 0.15 0.3 0.15 0.01 2 normal
execute if score #kt dv.dev matches 100 at @a[tag=dv_kpart,limit=1,sort=random] positioned ^ ^ ^-30 positioned over motion_blocking_no_leaves run function canon:alto/spawn
execute if score #kt dv.dev matches 1920 run playsound canon:music.bosque music @a[tag=dv_kpart] ~ ~ ~ 1 1
execute if score #kt dv.dev matches 3840 run playsound canon:music.bosque music @a[tag=dv_kpart] ~ ~ ~ 1 1
execute as @a[tag=dv_kpart] at @s if predicate canon:azar/1en100 run function canon:kevin/bosque/ambient
execute if score #kt dv.dev matches 6000.. run function canon:kevin/bosque/fail
''')
    pick('kevin/bosque/ambient', [
        'playsound canon:bosque.rama ambient @s ^ ^ ^-6 1 1',
        'playsound canon:bosque.pasos ambient @s ^3 ^ ^-5 1 1',
        'playsound canon:bosque.buho ambient @s ^-10 ^4 ^6 0.8 1',
        'playsound canon:bosque.viento ambient @s ~ ~ ~ 0.5 1',
        'playsound canon:alto.silbido ambient @s ^ ^ ^-25 0.6 1',
    ])
    F('kevin/bosque/nota_taken', '''
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=item_display,tag=dv_nota_vis] if score @s dv.id = #id dv.tmp run kill @s
scoreboard players add #knotes dv.dev 1
playsound canon:fx.sub_hit master @a[tag=dv_kpart] ~ ~ ~ 0.8 1
playsound canon:miron.estatica ambient @a[tag=dv_talker] ~ ~ ~ 1 1
function canon:kevin/bosque/nota_text
title @a[tag=dv_kpart] actionbar [{"text":"Notas: ","color":"gray"},{"score":{"name":"#knotes","objective":"dv.dev"},"color":"white"},{"text":"/6","color":"gray"}]
execute if score #knotes dv.dev matches 6.. run function canon:kevin/bosque/win
kill @s
''')
    pick('kevin/bosque/nota_text', ['tellraw @a[tag=dv_kpart] ' + jt('La nota dice: «' + t + '»', '#d8d8d8', True) for t in NOTAS])
    F('kevin/bosque/win', '''
execute as @e[type=zombie,tag=dv_alto] at @s run function canon:alto/vanish
stopsound @a[tag=dv_kpart] music canon:music.bosque
effect clear @a[tag=dv_kpart] minecraft:darkness
execute at @a[tag=dv_talker,limit=1] run function canon:kevin/arrive_here
execute if score #kprog dv.dev matches ..2 run scoreboard players set #kprog dv.dev 3
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/bosque/win_kevin
function canon:kevin/bosque/cleanup
''')
    F('kevin/bosque/win_kevin', chat('Kevin', '#ffb347', '¡LO GRABÉ TODO! ... ay no. La cámara solo grabó estática. Jajaja. Bueno, tengo otra idea.', '@a[distance=..40]') + '\nfunction canon:kevin/laugh')
    F('kevin/arrive_here', '''
scoreboard players set #ok dv.tmp 0
execute unless entity @e[type=zombie,tag=dv_kevin] positioned ^ ^ ^3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/summon
kill @e[type=marker,tag=dv_spot]
''')
    F('kevin/bosque/fail', '''
execute as @e[type=zombie,tag=dv_alto] at @s run function canon:alto/vanish
stopsound @a music canon:music.bosque
execute at @e[type=marker,tag=dv_bosque_c,limit=1] at @a[distance=..140,limit=1,sort=nearest] run function canon:kevin/arrive_here
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/bosque/fail_kevin
function canon:kevin/bosque/cleanup
''')
    F('kevin/bosque/fail_kevin', chat('Kevin', '#ffb347', 'Bro... ¿estás bien? Estabas gritando. Mejor lo intentamos otra noche.', '@a[distance=..60]'))
    F('kevin/bosque/cleanup', '''
kill @e[type=item_display,tag=dv_nota_vis]
kill @e[type=interaction,tag=dv_nota]
kill @e[type=marker,tag=dv_bosque_c]
execute as @e[type=zombie,tag=dv_alto] at @s run function canon:rig/despawn
tag @a remove dv_kpart
scoreboard players set #kev dv.dev 0
''')

    # ---- el Alto
    F('alto/spawn', rig_summon(['dv_alto'], 'El Alto', '#d8d8d8', head=False, scale=1.6) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_alto,distance=..2,limit=1,sort=nearest] at @s run function canon:alto/init')
    F('alto/init', f'''
function canon:rig/init_common
{set_cmd('body', CMD['alto_idle'])}
scoreboard players set @s dv.watch 0
playsound canon:alto.aparece hostile @a[tag=dv_kpart] ~ ~ ~ 0.6 0.8
''')
    F('alto/tick', '''
tag @s remove dv_xwalk
tag @a remove dv_wtgt
tag @a remove dv_lookers
tag @a[tag=dv_kpart,distance=..160,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_kpart] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:alto/vanish
execute if entity @a[tag=dv_wtgt] run function canon:alto/think
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('alto/think', '''
function canon:x/seen
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players add @s dv.timer 1
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score #seen dv.tmp matches 0 if score @s dv.watch matches 1.. run scoreboard players remove @s dv.watch 1
execute if score #seen dv.tmp matches 1 if score #m20 dv.clock matches 0 run function canon:alto/stare_fx
execute if score #seen dv.tmp matches 0 if entity @a[tag=dv_wtgt,distance=3..] run function canon:x/creep
scoreboard players set #aint dv.tmp 160
scoreboard players operation #an dv.tmp = #knotes dv.dev
scoreboard players operation #an dv.tmp *= #20 dv.math
scoreboard players operation #aint dv.tmp -= #an dv.tmp
execute if score #seen dv.tmp matches 0 if score @s dv.timer >= #aint dv.tmp run function canon:alto/blink
execute if score @s dv.watch matches 80.. run function canon:alto/lunge
tag @s remove dv_areach
execute if entity @a[tag=dv_wtgt,distance=..4] run tag @s add dv_areach
execute if entity @a[tag=dv_wtgt,distance=..1.8] run function canon:alto/catch
''')
    F('alto/stare_fx', '''
effect give @a[tag=dv_lookers,distance=..48] minecraft:darkness 2 0 true
playsound canon:miron.estatica ambient @a[tag=dv_lookers,distance=..48] ~ ~ ~ 0.7 0.8
''')
    F('alto/blink', '''
scoreboard players set @s dv.timer 0
scoreboard players set #ad dv.tmp 18
scoreboard players operation #an dv.tmp = #knotes dv.dev
scoreboard players operation #an dv.tmp *= #2 dv.math
scoreboard players operation #ad dv.tmp -= #an dv.tmp
execute if score #ad dv.tmp matches ..8 at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-8 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute if score #ad dv.tmp matches 9..12 at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-12 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute if score #ad dv.tmp matches 13.. at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-18 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute at @s run playsound canon:alto.pasos hostile @a[tag=dv_wtgt] ~ ~ ~ 0.9 0.8
''')
    F('alto/lunge', '''
scoreboard players set @s dv.watch 0
execute at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^2 run tp @s ~ ~ ~
playsound canon:alto.golpe hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.7
''')
    F('alto/catch', '''
playsound canon:alto.aparece master @a[tag=dv_wtgt] ~ ~ ~ 1 1
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
damage @a[tag=dv_wtgt,limit=1] 10 minecraft:mob_attack by @s
effect give @a[tag=dv_wtgt] minecraft:blindness 3 0 true
tellraw @a[tag=dv_wtgt] {"text":"No tenía cara. Pero sonreía.","color":"#d8d8d8","italic":true}
tag @a[tag=dv_wtgt] remove dv_kpart
scoreboard players set @s dv.timer 0
execute at @a[tag=dv_kpart,limit=1,sort=random] positioned ^ ^ ^-24 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
''')
    F('alto/vanish', '''
particle minecraft:large_smoke ~ ~1.5 ~ 0.3 1.2 0.3 0.02 30 normal
playsound canon:miron.estatica hostile @a[distance=..32] ~ ~ ~ 1 0.6
function canon:rig/despawn
''')


def gen_cata():
    # ------- laberinto (fijo) en el overworld profundo, lejos de todo
    X0, Z0, Y0 = 20000, 20000, -50
    N = 8
    C = 5  # celda: 3 de pasillo + 2 de muro
    W = N * C + 2
    rng = random.Random(7)
    vis = [[False] * N for _ in range(N)]
    walls = set()
    for i in range(N):
        for j in range(N):
            for d in ((1, 0), (0, 1)):
                walls.add(((i, j), (i + d[0], j + d[1])))
    stack = [(0, 0)]
    vis[0][0] = True
    order = {(0, 0): 0}
    while stack:
        i, j = stack[-1]
        nb = [(i + a, j + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= i + a < N and 0 <= j + b < N and not vis[i + a][j + b]]
        if not nb:
            stack.pop()
            continue
        n = rng.choice(nb)
        vis[n[0]][n[1]] = True
        order[n] = len(stack)
        a, b = sorted([(i, j), n])
        walls.discard((a, b))
        stack.append(n)
    # celda de la llave: la más profunda que no sea la salida
    exitc = (N - 1, N - 1)
    keyc = max((c for c in order if c != exitc and c != (0, 0)), key=lambda c: order[c])

    def cell_origin(c):
        return X0 + 2 + c[0] * C, Z0 + 2 + c[1] * C

    cmds = []
    y1, y2 = Y0, Y0 + 7
    cmds.append(f'fill {X0} {y1} {Z0} {X0 + W + 8} {y2} {Z0 + W} minecraft:deepslate_bricks')
    for i in range(N):
        for j in range(N):
            x, z = cell_origin((i, j))
            cmds.append(f'fill {x} {Y0 + 1} {z} {x + 2} {Y0 + 4} {z + 2} minecraft:air')
            if ((i, j), (i + 1, j)) not in walls and i + 1 < N:
                cmds.append(f'fill {x + 3} {Y0 + 1} {z} {x + 4} {Y0 + 4} {z + 2} minecraft:air')
            if ((i, j), (i, j + 1)) not in walls and j + 1 < N:
                cmds.append(f'fill {x} {Y0 + 1} {z + 3} {x + 2} {Y0 + 4} {z + 4} minecraft:air')
    # suelo y techo variados
    cmds.append(f'fill {X0} {Y0} {Z0} {X0 + W} {Y0} {Z0 + W} minecraft:deepslate_tiles')
    cmds.append(f'fill {X0} {Y0 + 5} {Z0} {X0 + W} {Y0 + 5} {Z0 + W} minecraft:cracked_deepslate_tiles')
    deco = []
    for i in range(N):
        for j in range(N):
            x, z = cell_origin((i, j))
            r = rng.random()
            if r < 0.18:
                deco.append(f'setblock {x + rng.randint(0, 2)} {Y0 + 1} {z + rng.randint(0, 2)} minecraft:skeleton_skull[rotation={rng.randint(0, 15)}]')
            elif r < 0.30:
                deco.append(f'setblock {x + rng.choice([0, 2])} {Y0 + 4} {z + rng.choice([0, 2])} minecraft:cobweb')
            elif r < 0.40:
                deco.append(f'setblock {x + 1} {Y0 + 4} {z + 1} minecraft:soul_lantern[hanging=true]')
            elif r < 0.48:
                deco.append(f'setblock {x + rng.choice([0, 2])} {Y0 + 1} {z + rng.choice([0, 2])} minecraft:bone_block')
            elif r < 0.56:
                deco.append(f'setblock {x + rng.randint(0, 2)} {Y0 + 1} {z + rng.randint(0, 2)} minecraft:candle[candles=3,lit=true]')
            for _ in range(2):
                xx, yy, zz = x + rng.choice([-1, 3]), Y0 + rng.randint(1, 4), z + rng.randint(0, 2)
                deco.append(f'fill {xx} {yy} {zz} {xx} {yy} {zz} minecraft:cracked_deepslate_bricks replace minecraft:deepslate_bricks')
    sx, sz = cell_origin((0, 0))
    ex, ez = cell_origin(exitc)
    kx, kz = cell_origin(keyc)
    # salida: pasillo extra al este de la celda final, con reja
    cmds2 = [
        f'fill {ex + 3} {Y0 + 1} {ez} {ex + 6} {Y0 + 4} {ez + 2} minecraft:air',
        f'fill {ex + 3} {Y0 + 1} {ez} {ex + 3} {Y0 + 3} {ez + 2} minecraft:iron_bars',
        f'setblock {ex + 6} {Y0 + 2} {ez + 1} minecraft:soul_lantern',
        f'setblock {sx + 1} {Y0 + 4} {sz + 1} minecraft:soul_lantern[hanging=true]',
    ]
    F('kevin/cata/build_place', '\n'.join(cmds + deco + cmds2) + '\nscoreboard players set #cata_built dv.build 2\n'
      f'forceload remove {X0} {Z0} {X0 + W + 8} {Z0 + W}')
    F('kevin/cata/build_try', f'execute in minecraft:overworld if loaded {X0} {Y0} {Z0} if loaded {X0 + W + 8} {Y0} {Z0 + W} if loaded {X0} {Y0} {Z0 + W} if loaded {X0 + W + 8} {Y0} {Z0} in minecraft:overworld run function canon:kevin/cata/build_place')
    F('kevin/cata/build_start', f'''
scoreboard players set #cata_built dv.build 1
execute in minecraft:overworld run forceload add {X0} {Z0} {X0 + W + 8} {Z0 + W}
''')
    sel_in = f'x={X0 - 2},y={Y0 - 2},z={Z0 - 2},dx={W + 12},dy=12,dz={W + 4}'
    F('kevin/cata/try', f'''
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
execute unless score #kev dv.dev matches 1.. run function canon:kevin/cata/prep
''')
    F('kevin/cata/prep', f'''
scoreboard players set #kev dv.dev 3
scoreboard players set #kt dv.dev -100000
scoreboard players set #ckey dv.dev 0
tag @a[gamemode=!spectator,distance=..32] add dv_kpart
execute if score #cata_built dv.build matches 0 run function canon:kevin/cata/build_start
{kv_say('Síganme. Y no toquen los huesos. Bueno, tóquenlos si quieren, pero después no lloren.', 120, '@a[tag=dv_kpart]')}
tellraw @a[tag=dv_kpart] {jt('(Bajando a las catacumbas...)', 'gray', True)}
schedule function canon:kevin/cata/enter_wait 40t replace
''')
    F('kevin/cata/enter_wait', '''
execute if score #cata_built dv.build matches 2 run function canon:kevin/cata/enter
execute unless score #cata_built dv.build matches 2 if score #kev dv.dev matches 3 run schedule function canon:kevin/cata/enter_wait 20t replace
''')
    F('kevin/cata/enter', f'''
scoreboard players set #kt dv.dev 0
execute as @a[tag=dv_kpart] at @s run function canon:travel/store_return
execute as @a[tag=dv_kpart] in minecraft:overworld run tp @s {sx + 1}.5 {Y0 + 1} {sz + 1}.5 -90 0
execute as @a[tag=dv_kpart] run effect give @s minecraft:darkness 3 0 true
execute as @e[type=zombie,tag=dv_kevin] in minecraft:overworld run tp @s {sx + 1}.5 {Y0 + 1} {sz + 0}.5
playsound canon:cata.reja master @a[tag=dv_kpart] ~ ~ ~ 1 0.8
playsound canon:cata.ambient ambient @a[tag=dv_kpart] ~ ~ ~ 1 1
title @a[tag=dv_kpart] times 10 60 20
title @a[tag=dv_kpart] subtitle {{"text":"Encuentra la llave de la reja. Algo se arrastra ahí abajo.","color":"gray","italic":true}}
title @a[tag=dv_kpart] title {{"text":"LAS CATACUMBAS","color":"#9a9a9a"}}
kill @e[type=interaction,tag=dv_cllave]
kill @e[type=item_display,tag=dv_cllave_vis]
kill @e[type=interaction,tag=dv_creja]
execute in minecraft:overworld run summon minecraft:item_display {kx + 1}.5 {Y0 + 1}.4 {kz + 1}.5 {{Tags:["dv_cllave_vis"],brightness:{{sky:12,block:12}},billboard:"vertical",item:{{id:"minecraft:tripwire_hook",Count:1b}},transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f],right_rotation:[0f,0f,0f,1f]}}}}
execute in minecraft:overworld run summon minecraft:interaction {kx + 1}.5 {Y0 + 1} {kz + 1}.5 {{Tags:["dv_cllave","dv_click","dv_npc_click"],width:1.0f,height:1.0f,response:1b}}
execute in minecraft:overworld run summon minecraft:interaction {ex + 3}.5 {Y0 + 1} {ez + 1}.5 {{Tags:["dv_creja","dv_click","dv_npc_click"],width:1.2f,height:3.0f,response:1b}}
execute in minecraft:overworld run fill {ex + 3} {Y0 + 1} {ez} {ex + 3} {Y0 + 3} {ez + 2} minecraft:iron_bars
''')
    F('kevin/cata/tick', f'''
execute if score #kt dv.dev matches 0.. run function canon:kevin/cata/tick2
''')
    F('kevin/cata/tick2', f'''
execute as @a[tag=dv_kpart] unless entity @s[{sel_in}] run tag @s remove dv_kpart
execute unless entity @a[tag=dv_kpart] run function canon:kevin/cata/fail
execute if score #kt dv.dev matches 400 in minecraft:overworld positioned {sx + 1}.5 {Y0 + 1} {sz + 1}.5 run function canon:masa/spawn
execute if score #kt dv.dev matches 560 run playsound canon:masa.rugido hostile @a[tag=dv_kpart] ~ ~ ~ 1 0.8
execute if score #kt dv.dev matches 560 run tellraw @a[tag=dv_kpart] {jt('Algo enorme se mueve detrás de ustedes. Respira.', '#9a9a9a', True)}
scoreboard players operation #c dv.tmp = #kt dv.dev
scoreboard players operation #c dv.tmp %= #560 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:cata.ambient ambient @a[tag=dv_kpart] ~ ~ ~ 1 1
execute as @a[tag=dv_kpart] at @s if predicate canon:azar/1en600 run playsound canon:cata.derrumbe ambient @s ^ ^ ^-8 0.8 1
execute if score #m40 dv.clock matches 0 as @e[type=item_display,tag=dv_cllave_vis] at @s run particle minecraft:soul ~ ~0.3 ~ 0.1 0.2 0.1 0.01 1 normal
execute as @a[tag=dv_kpart] at @s if entity @s[x={ex + 5},y={Y0},z={ez},dx=2,dy=4,dz=3] run function canon:kevin/cata/player_out
execute if score #kt dv.dev matches 12000.. run function canon:kevin/cata/fail
''')
    F('kevin/cata/clicked', kv_say('Busquen la llave. Debe estar en el rincón más lejano. Siempre está en el rincón más lejano.', 100))
    F('kevin/cata/llave_taken', '''
scoreboard players set #ckey dv.dev 1
kill @e[type=item_display,tag=dv_cllave_vis]
playsound canon:cata.reja master @a[tag=dv_kpart] ~ ~ ~ 0.6 1.4
tellraw @a[tag=dv_kpart] [{"selector":"@a[tag=dv_talker]","color":"#e8c9a8"},{"text":" encontró una llave oxidada. Ahora: la reja.","color":"#9a9a9a","italic":true}]
kill @s
''')
    F('kevin/cata/reja_used', f'''
execute if score #ckey dv.dev matches 0 run tellraw @a[tag=dv_talker] {jt('La reja está cerrada con candado. Necesitan una llave.', '#9a9a9a', True)}
execute if score #ckey dv.dev matches 0 run playsound canon:cata.reja master @a[tag=dv_talker] ~ ~ ~ 0.5 0.6
execute if score #ckey dv.dev matches 1 run function canon:kevin/cata/open
''')
    F('kevin/cata/open', f'''
execute in minecraft:overworld run fill {ex + 3} {Y0 + 1} {ez} {ex + 3} {Y0 + 3} {ez + 2} minecraft:air
playsound canon:cata.reja master @a[tag=dv_kpart] ~ ~ ~ 1 1
tellraw @a[tag=dv_kpart] {jt('La reja chirría y se abre. Hay una escalera al fondo. ¡Corran!', '#e8c9a8', True)}
kill @s
''')
    F('kevin/cata/player_out', f'''
tag @s add dv_cout
tag @s remove dv_kpart
function canon:util/tp_return
effect give @s minecraft:darkness 3 0 true
stopsound @s ambient canon:cata.ambient
execute unless entity @a[tag=dv_kpart] run function canon:kevin/cata/win
''')
    F('kevin/cata/win', f'''
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
playsound canon:cata.derrumbe master @a[tag=dv_cout] ~ ~ ~ 1 0.8
tellraw @a[tag=dv_cout] {jt('Detrás de ustedes, el túnel se derrumba. Kevin gritaba: «¡Vayan, ya los alcanzo!»', '#9a9a9a', True)}
execute if score #kprog dv.dev matches ..3 run tellraw @a[tag=dv_cout] {jt('Kevin no salió.', '#c94a4a', True)}
execute if score #kprog dv.dev matches 5.. run tellraw @a[tag=dv_cout] {jt('Un rato después, Kevin sale de una alcantarilla, lleno de polvo, riéndose.', '#ffb347', True)}
execute if score #kprog dv.dev matches 5.. run scoreboard players set #kevcd dv.dev 30
execute if score #kprog dv.dev matches ..3 run function canon:kevin/dias/begin
tag @a remove dv_cout
function canon:kevin/cata/cleanup
''')
    F('kevin/cata/fail', f'''
execute as @a[{sel_in}] at @s run function canon:util/tp_return
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
tellraw @a[tag=dv_kpart] {jt('Las catacumbas los escupen afuera. Kevin quedó abajo... por ahora.', '#9a9a9a', True)}
scoreboard players set #kevcd dv.dev 600
function canon:kevin/cata/cleanup
''')
    F('kevin/cata/cleanup', '''
execute as @e[type=zombie,tag=dv_masa] at @s run function canon:rig/despawn
kill @e[type=interaction,tag=dv_cllave]
kill @e[type=item_display,tag=dv_cllave_vis]
kill @e[type=interaction,tag=dv_creja]
tag @a remove dv_kpart
tag @a remove dv_cout
scoreboard players set #kev dv.dev 0
''')
    # la Masa
    F('masa/spawn', rig_summon(['dv_masa'], 'La Masa', '#8e3b3f', head=False, scale=1.4) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_masa,distance=..2,limit=1,sort=nearest] at @s run function canon:masa/init')
    F('masa/init', f'''
function canon:rig/init_common
{set_cmd('body', CMD['masa_idle'])}
playsound canon:masa.rugido hostile @a[distance=..48] ~ ~ ~ 1 0.7
''')
    F('masa/tick', '''
tag @a remove dv_wtgt
tag @a[tag=dv_kpart,distance=..80,limit=1,sort=nearest] add dv_wtgt
execute unless score #kev dv.dev matches 3 run function canon:rig/despawn
execute if entity @a[tag=dv_wtgt] run function canon:masa/think
tag @a remove dv_wtgt
''')
    F('masa/think', '''
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.085 run tp @s ~ ~ ~ ~ ~
scoreboard players add @s dv.timer 1
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #40 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:masa.arrastre hostile @a[distance=..24] ~ ~ ~ 1 1
execute if score #c dv.tmp matches 0 run particle minecraft:block minecraft:redstone_block ~ ~0.3 ~ 0.6 0.2 0.6 0 12 normal
scoreboard players remove @s[scores={dv.timer2=1..}] dv.timer2 1
execute if entity @a[tag=dv_wtgt,distance=..1.8] unless score @s dv.timer2 matches 1.. run function canon:masa/hit
''')
    F('masa/hit', '''
scoreboard players set @s dv.timer2 25
damage @a[tag=dv_wtgt,limit=1] 6 minecraft:mob_attack by @s
effect give @a[tag=dv_wtgt] minecraft:slowness 3 2 true
playsound canon:masa.rugido hostile @a[distance=..16] ~ ~ ~ 1 1.3
''')
    return sx, sz, X0, Z0, Y0


def gen_dias():
    K = CMD
    F('kevin/dias/begin', '''
scoreboard players set #kprog dv.dev 4
scoreboard players set #kdays dv.dev 1
execute store result score #kday_last dv.dev run time query day
scoreboard players set #kfakecd dv.dev 120
''')
    F('kevin/dias/second', f'''
execute store result score #kday dv.tmp run time query day
execute unless score #kday dv.tmp = #kday_last dv.dev run function canon:kevin/dias/new_day
execute if score #kfakecd dv.dev matches 1.. run scoreboard players remove #kfakecd dv.dev 1
execute if score #kfakecd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_kfake] as @a[gamemode=!spectator,predicate=canon:en_superficie,predicate=canon:de_noche,limit=1,sort=random] at @s if predicate canon:azar/1en60 run function canon:kevin/dias/fake_spawn
''')
    F('kevin/dias/new_day', f'''
scoreboard players operation #kday_last dv.dev = #kday dv.tmp
scoreboard players add #kdays dv.dev 1
execute if score #kdays dv.dev matches 2 run tellraw @a {jt('Día 2 sin Kevin. Su celular suena apagado. De noche alguien grita tu nombre con su voz.', '#ffb347', True)}
execute if score #kdays dv.dev matches 3 run tellraw @a {jt('Día 3. Encuentras una gorra negra en la puerta, mojada de barro. Esta noche no salgas.', '#ffb347', True)}
execute if score #kdays dv.dev matches 4.. run function canon:kevin/dias/return
''')
    F('kevin/dias/return', f'''
scoreboard players set #kprog dv.dev 5
scoreboard players set #kdays dv.dev 0
scoreboard players set #kevcd dv.dev 0
execute as @e[type=zombie,tag=dv_kfake] at @s run function canon:rig/despawn
execute as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s run function canon:kevin/dias/return_here
''')
    F('kevin/dias/return_here', f'''
function canon:kevin/arrive_here
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/dias/return_say
''')
    F('kevin/dias/return_say', chat('Kevin', '#ffb347', '¡EYYYY! ¿Me extrañaron? Tres días perdido. Salí por una alcantarilla. Comí cosas que no voy a contar. Jajaja.', '@a') + '''
playsound canon:kevin.hey neutral @a[distance=..32] ~ ~1.6 ~ 1 1
function canon:kevin/laugh
title @a times 10 70 20
title @a subtitle {"text":"Ahora es más chistoso que nunca. Lástima.","color":"#ffd27a","italic":true}
title @a title {"text":"KEVIN VOLVIÓ","color":"#ffb347","bold":true}
''')
    F('kevin/dias/fake_spawn', '''
scoreboard players set #kfakecd dv.dev 240
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^22 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^ ^ ^-18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/dias/fake_summon
kill @e[type=marker,tag=dv_spot]
''')
    F('kevin/dias/fake_summon', rig_summon(['dv_kfake'], 'Kevin', '#ffb347') + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_kfake,distance=..2,limit=1,sort=nearest] at @s run function canon:kevin/dias/fake_init')
    F('kevin/dias/fake_init', f'''
function canon:rig/init_common
{set_cmd('body', K['kevin_idle'])}
{head(K['kevin_cabeza_neutral'])}
function canon:x/add_bubble
''')
    F('kevin/dias/fake_tick', f'''
function canon:x/links_follow
tag @a remove dv_wtgt
tag @a[gamemode=!spectator,distance=..64,limit=1,sort=nearest] add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players add @s dv.timer 1
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #60 dv.math
execute if score #c dv.tmp matches 1 run playsound canon:kevin.hey hostile @a[distance=..48] ~ ~1.6 ~ 1 0.92
execute if score #c dv.tmp matches 1 run function canon:kevin/dias/fake_call
execute if entity @a[tag=dv_wtgt,distance=..7] run function canon:kevin/dias/fake_reveal
execute if score @s dv.timer matches 800.. run function canon:rig/vanish
tag @a remove dv_wtgt
''')
    F('kevin/dias/fake_call', bubble('dv_xbubble', '¡Eyy! ¡Por aquí! ¡Ven!', '#ffd27a', 50))
    F('kevin/dias/fake_reveal', f'''
{head(K['kevin_cabeza_drogado'])}
playsound canon:miron.grito master @a[distance=..12] ~ ~ ~ 1 0.8
execute as @a[distance=..12] at @s run function canon:x/jumpscare
tellraw @a[distance=..12] {jt('Eso no era Kevin.', '#c94a4a', True)}
function canon:rig/vanish
''')


# =================================================================== NICOLÁS

INSULTOS = [
    'Nadie te va a extrañar aquí abajo.',
    'Cava, cava... estás cavando tu propia tumba.',
    '¿Crees que eres especial? Eres un chiste.',
    'Todos se ríen de ti cuando no estás.',
    'Mírate. Das pena.',
    'Aquí abajo nadie oye tus gritos.',
    'Eres lento. Eres débil. Eres mío.',
    'Tus amigos ya se fueron sin ti.',
    'Hueles a miedo.',
    'No eres nadie. Nunca lo fuiste.',
    '¿Por qué sigues intentando? Ya perdiste.',
    'Corre, gordito... ah no, ese soy yo. Jajaja.',
]


def gen_nicolas():
    K = CMD
    F('nicolas/try', '''
scoreboard players set @s dv.ncd 420
execute if entity @e[type=zombie,tag=dv_nicolas,distance=..96] run scoreboard players set @s dv.ncd 60
execute unless entity @e[type=zombie,tag=dv_nicolas,distance=..96] run function canon:nicolas/try2
''')
    F('nicolas/try2', f'''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^ ^ ^-8 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:nicolas/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run tellraw @s {jt('Pasos pesados detrás de ti. Alguien se ríe bajito.', '#8a8a96', True)}
execute if score #ok dv.tmp matches 1 run playsound canon:nicolas.risa hostile @s ^ ^ ^-10 1 0.9
execute if score #ok dv.tmp matches 1 run playsound canon:mina.ambient ambient @s ~ ~ ~ 0.8 1
execute if score #ok dv.tmp matches 1 as @e[type=wolf,tag=dv_luna,distance=..24] at @s run function canon:luna/n/nicolas
''')
    F('nicolas/summon', rig_summon(['dv_nicolas'], 'Nicolás', '#8a8a96', health=40, invul=False) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_nicolas,distance=..2,limit=1,sort=nearest] at @s run function canon:nicolas/init')
    F('nicolas/init', f'''
function canon:rig/init_common
{set_cmd('body', K['nicolas_idle'])}
{head(K['nicolas_cabeza_burla'])}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.say -1
scoreboard players set @s dv.timer2 60
function canon:x/add_bubble
''')
    F('nicolas/tick', '''
function canon:x/links_follow
tag @s remove dv_xwalk
tag @s remove dv_nreach
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
scoreboard players operation #tgt dv.tmp = @s dv.target
tag @a remove dv_wtgt
execute as @a[distance=..48,gamemode=!spectator] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
scoreboard players add @s dv.timer 1
scoreboard players set #ngo dv.tmp 0
execute unless entity @a[tag=dv_wtgt] run scoreboard players set #ngo dv.tmp 1
execute if entity @a[tag=dv_wtgt,y=56,dy=400] run scoreboard players set #ngo dv.tmp 1
execute if score @s dv.timer matches 1400.. run scoreboard players set #ngo dv.tmp 1
execute if score #ngo dv.tmp matches 0 run function canon:nicolas/hunt
execute if score #ngo dv.tmp matches 1 run function canon:nicolas/leave
tag @a remove dv_wtgt
''')
    F('nicolas/hunt', f'''
execute if entity @a[tag=dv_wtgt,distance=1.5..] run function canon:nicolas/step
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #90 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:nicolas.pasos hostile @a[distance=..24] ~ ~ ~ 1 0.9
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #140 dv.math
execute if score #c dv.tmp matches 20 run function canon:nicolas/insult
scoreboard players remove @s[scores={{dv.timer2=1..}}] dv.timer2 1
execute if entity @a[tag=dv_wtgt,distance=..3] run tag @s add dv_nreach
execute if entity @a[tag=dv_wtgt,distance=..1.6] unless score @s dv.timer2 matches 1.. run function canon:nicolas/hit
''')
    F('nicolas/step', '''
tag @s add dv_xwalk
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.15 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
''')
    opts = []
    for i, t in enumerate(INSULTOS):
        h = K['nicolas_cabeza_odio'] if i % 2 else K['nicolas_cabeza_burla']
        opts.append(bubble('dv_xbubble', t, '#b9b9c6', 80) + '\n' + chat('Nicolás', '#8a8a96', t, '@a[tag=dv_wtgt]') + '\n' + head(h))
    pick('nicolas/insult', opts)
    F('nicolas/hit', f'''
scoreboard players set @s dv.timer2 24
damage @a[tag=dv_wtgt,limit=1] 3 minecraft:mob_attack by @s
playsound canon:nicolas.risa hostile @a[distance=..16] ~ ~ ~ 1 1.1
{head(K['nicolas_cabeza_grito'])}
''')
    F('nicolas/leave', '''
playsound canon:nicolas.risa hostile @a[distance=..24] ~ ~ ~ 0.8 0.8
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.7 0.3 0.01 20 normal
function canon:rig/despawn
''')
    F('nicolas/died', f'''
playsound canon:nicolas.risa hostile @a[distance=..24] ~ ~ ~ 1 0.6
tellraw @a[distance=..24] {jt('Nicolás se deshace en humo negro. Su risa sigue sonando en la piedra.', '#8a8a96', True)}
''')
    # susto al picar piedra
    F('nicolas/mined', '''
scoreboard players set @s dv.mst 0
scoreboard players set @s dv.mds 0
execute if score #nicolas dv.cfg matches 1 if predicate canon:en_superficie if entity @s[y=-64,dy=114] unless score @s dv.ncd matches 61.. if predicate canon:azar/1en150 run function canon:nicolas/face_scare
''')
    F('nicolas/face_scare', f'''
scoreboard players set @s dv.ncd 900
execute anchored eyes positioned ^ ^ ^2.4 run summon minecraft:item_display ~ ~ ~ {{Tags:["dv_nface","dv_nface_new"],item_display:"none",brightness:{{sky:15,block:12}},view_range:0.6f,item:{{id:"minecraft:leather_horse_armor",Count:1b,tag:{{CustomModelData:{K['nicolas_cabeza_grito']}}}}},transformation:{{translation:[0f,-0.12f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f],right_rotation:[0f,0f,0f,1f]}}}}
tag @s add dv_nface_me
execute as @e[type=item_display,tag=dv_nface_new] at @s facing entity @a[tag=dv_nface_me,limit=1] eyes run tp @s ~ ~ ~ ~ 0
tag @s remove dv_nface_me
execute if score #flip dv.cfg matches 1 as @e[type=item_display,tag=dv_nface_new] run data modify entity @s transformation.right_rotation set value [0f,1f,0f,0f]
execute as @e[type=item_display,tag=dv_nface_new] run data merge entity @s {{start_interpolation:0,interpolation_duration:3,transformation:{{scale:[2.4f,2.4f,2.4f],translation:[0f,-0.5f,0f]}}}}
tag @e[type=item_display,tag=dv_nface_new] remove dv_nface_new
playsound canon:nicolas.maldito master @s ~ ~ ~ 1 0.95
playsound canon:fx.stinger master @s ~ ~ ~ 0.9 1
effect give @s minecraft:darkness 3 0 true
title @s times 0 25 10
title @s subtitle {{"text":"¡MALDITO!","color":"#b01212","bold":true}}
title @s title {{"text":" "}}
function canon:fx/shake_big
''')
    F('nicolas/face_tick', '''
scoreboard players add @s dv.timer 1
execute if score @s dv.timer matches 22 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[0f,0f,0f]}}
execute if score @s dv.timer matches 22 run particle minecraft:large_smoke ~ ~ ~ 0.4 0.4 0.4 0.02 20 normal
execute if score @s dv.timer matches 32.. run kill @s
''')


# =================================================================== MIRÓN

def gen_miron():
    F('miron/try', '''
execute if score #mironcd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_miron] run function canon:miron/try2
''')
    F('miron/try2', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^20 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^6 ^ ^16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^-6 ^ ^14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:miron/spawn_here
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run function canon:miron/announce
''')
    F('miron/announce', '''
scoreboard players set #mironcd dv.dev 420
playsound canon:miron.aparece ambient @s ~ ~ ~ 0.9 0.9
playsound canon:fx.heartbeat ambient @s ~ ~ ~ 0.7 1
execute as @e[type=wolf,tag=dv_luna,distance=..24] at @s run function canon:luna/alarm_watch
''')
    F('miron/spawn_here', rig_summon(['dv_miron'], '???', '#2a272d', head=False, scale=1.3) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_miron,distance=..2,limit=1,sort=nearest] at @s run function canon:miron/init')
    F('miron/init', f'''
function canon:rig/init_common
{set_cmd('body', CMD['miron_idle'])}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.watch 0
''')
    F('miron/tick', '''
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..80] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..48,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_wtgt] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:miron/gone
execute if entity @a[tag=dv_wtgt] run function canon:miron/think
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('miron/think', '''
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players add @s dv.timer 1
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #60 dv.math
execute if score #c dv.tmp matches 0..29 run tag @s add dv_mpeek
execute if score #c dv.tmp matches 30.. run tag @s remove dv_mpeek
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #80 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:miron.respira hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.9
execute if score @s dv.watch matches 12.. run function canon:miron/seen_react
execute if entity @a[tag=dv_wtgt,distance=..8] run function canon:miron/close_react
execute if score @s dv.timer matches 300.. run function canon:miron/gone
''')
    pick('miron/seen_react', [
        'playsound canon:miron.estatica hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.8\nfunction canon:miron/gone',
        'playsound canon:miron.estatica hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.6\nfunction canon:miron/gone',
        'playsound canon:miron.grito hostile @a[tag=dv_wtgt] ~ ~ ~ 1 1\nfunction canon:miron/gone',
    ])
    F('miron/close_react', '''
playsound canon:miron.grito master @a[tag=dv_wtgt] ~ ~ ~ 1 1
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
function canon:miron/gone
''')
    F('miron/gone', '''
particle minecraft:large_smoke ~ ~1.2 ~ 0.25 0.8 0.25 0.01 25 normal
function canon:rig/despawn
''')


# =================================================================== CASA BLANCA (sueño de los demás)

def gen_casa():
    # Casa de madera de 2 pisos con techo en punta y dos ventanas en el techo.
    # Mirando hacia la casa (hacia +z, sur): la izquierda es +x (este).
    B = []

    def fill(x1, y1, z1, x2, y2, z2, b, extra=''):
        B.append(f'fill {x1} {y1} {z1} {x2} {y2} {z2} minecraft:{b}{extra}')

    def sb(x, y, z, b):
        B.append(f'setblock {x} {y} {z} minecraft:{b}')

    G = 63  # bloque de suelo (concreto); se camina en 64
    F0 = 66  # piso planta baja (se camina en 67)
    F1 = 71  # piso segundo (se camina en 72)
    # limpiar
    fill(-14, 64, -10, 24, 79, 26, 'air')
    fill(-14, 80, -10, 24, 95, 26, 'air')
    # jardín (oeste) y patio delantero
    fill(-12, G, -8, 22, G, 22, 'grass_block')
    fill(-12, G, 6, -2, G, 20, 'grass_block')
    fill(4, G, -8, 13, G, -2, 'grass_block')
    fill(11, G, -8, 12, G, -3, 'gravel')
    # cerca delantera con reja (portón) a la izquierda
    fill(-1, 64, -7, 17, 64, -7, 'spruce_fence')
    fill(-1, 64, -7, -1, 64, -1, 'spruce_fence')
    fill(17, 64, -7, 17, 64, -1, 'spruce_fence')
    sb(12, 64, -7, 'spruce_fence_gate[facing=south]')
    sb(11, 64, -7, 'spruce_fence_gate[facing=south]')
    # cimiento
    fill(0, 64, 0, 16, 65, 15, 'cobblestone')
    fill(0, F0, 0, 16, F0, 15, 'spruce_planks')
    # porche delantero (z=-2..-1) a la altura del piso
    fill(6, 64, -2, 10, 65, -1, 'cobblestone')
    fill(6, F0, -2, 10, F0, -1, 'spruce_planks')
    # escalones que suben desde la izquierda hasta la puerta (al medio)
    fill(11, 64, -2, 13, 64, -1, 'cobblestone')
    fill(11, 65, -2, 12, 65, -1, 'cobblestone')
    fill(13, 64, -2, 13, 64, -1, 'spruce_stairs[facing=west]')
    fill(12, 65, -2, 12, 65, -1, 'spruce_stairs[facing=west]')
    fill(11, F0, -2, 11, F0, -1, 'spruce_stairs[facing=west]')
    fill(6, F0 + 1, -2, 6, F0 + 1, -1, 'spruce_fence')
    fill(7, F0 + 1, -2, 10, F0 + 1, -2, 'spruce_fence')
    sb(8, F0 + 1, -2, 'air')
    fill(8, F0 + 1, -2, 8, F0 + 1, -2, 'air')
    fill(6, F0 + 1, -2, 10, F0 + 1, -2, 'spruce_fence')
    fill(8, F0 + 1, -2, 10, F0 + 1, -2, 'air')
    fill(6, F0 + 1, -2, 7, F0 + 1, -2, 'spruce_fence')
    # paredes exteriores (dos pisos)
    fill(0, F0 + 1, 0, 16, F1 + 4, 15, 'birch_planks')
    fill(1, F0 + 1, 1, 15, F1 + 4, 14, 'air')
    for x, z in ((0, 0), (16, 0), (0, 15), (16, 15)):
        fill(x, F0 + 1, z, x, F1 + 4, z, 'stripped_spruce_log')
    fill(0, F1, 0, 16, F1, 15, 'stripped_spruce_log[axis=x]')
    # piso del segundo
    fill(1, F1, 1, 15, F1, 14, 'spruce_planks')
    # ---- planta baja
    # hall x 6..10, z 1..6; muros interiores
    fill(5, F0 + 1, 1, 5, F1 - 1, 6, 'birch_planks')      # muro cocina (derecha/oeste)
    fill(11, F0 + 1, 1, 11, F1 - 1, 6, 'birch_planks')    # muro cuarto (izquierda/este)
    fill(1, F0 + 1, 7, 15, F1 - 1, 7, 'birch_planks')     # muro salón
    # puerta principal
    sb(8, F0 + 1, 0, 'spruce_door[facing=south,half=lower,hinge=left]')
    sb(8, F0 + 2, 0, 'spruce_door[facing=south,half=upper,hinge=left]')
    # escalera a la derecha (x=6) subiendo hacia el fondo
    for k in range(5):
        sb(6, F0 + 1 + k, 2 + k, 'spruce_stairs[facing=south]')
        if k < 4:
            fill(6, F0 + 1, 2 + k, 6, F0 + k, 2 + k, 'spruce_planks') if k > 0 else None
    fill(6, F1, 2, 6, F1, 5, 'air')
    fill(7, F1 + 1, 2, 7, F1 + 1, 5, 'spruce_fence')
    # puerta de la cocina, justo al entrar a la derecha
    sb(5, F0 + 1, 1, 'spruce_door[facing=west,half=lower,hinge=right]')
    sb(5, F0 + 2, 1, 'spruce_door[facing=west,half=upper,hinge=right]')
    # puerta del cuarto (izquierda)
    sb(11, F0 + 1, 3, 'spruce_door[facing=east,half=lower,hinge=left]')
    sb(11, F0 + 2, 3, 'spruce_door[facing=east,half=upper,hinge=left]')
    # puerta al salón (de frente)
    sb(8, F0 + 1, 7, 'spruce_door[facing=south,half=lower,hinge=left]')
    sb(8, F0 + 2, 7, 'spruce_door[facing=south,half=upper,hinge=left]')
    # cocina x1..4 z1..6
    fill(1, F0 + 1, 6, 4, F0 + 1, 6, 'smooth_stone_slab[type=double]')
    sb(1, F0 + 1, 6, 'smoker[facing=north]')
    sb(2, F0 + 1, 6, 'cauldron')
    sb(4, F0 + 1, 6, 'barrel[facing=up]')
    fill(1, F0 + 1, 3, 1, F0 + 2, 3, 'iron_block')
    sb(3, F0 + 1, 3, 'spruce_fence')
    sb(3, F0 + 2, 3, 'spruce_pressure_plate')
    sb(3, F1 - 1, 3, 'lantern[hanging=true]')
    # cuarto de abajo x12..15 z1..6
    sb(14, F0 + 1, 5, 'white_bed[facing=south,part=foot]')
    sb(14, F0 + 1, 6, 'white_bed[facing=south,part=head]')
    fill(15, F0 + 1, 1, 15, F0 + 2, 2, 'bookshelf')
    sb(12, F0 + 1, 6, 'flower_pot')
    sb(13, F1 - 1, 3, 'lantern[hanging=true]')
    # hall
    sb(9, F0 + 1, 1, 'potted_fern')
    sb(9, F1 - 1, 4, 'lantern[hanging=true]')
    fill(8, F0, 1, 9, F0, 6, 'spruce_planks')
    # salón x1..15 z8..14
    # sofá gris a la izquierda (este, x=15), de la esquina (z=14) a la mitad (z=11)
    fill(15, F0 + 1, 11, 15, F0 + 1, 14, 'polished_andesite_stairs[facing=east]')
    sb(15, F0 + 1, 10, 'light_gray_wool')
    fill(15, F0 + 2, 11, 15, F0 + 2, 14, 'light_gray_carpet')
    fill(12, F0 + 1, 11, 13, F0 + 1, 13, 'gray_carpet')
    # televisor en la pared de enfrente (oeste, x=1)
    fill(1, F0 + 1, 11, 1, F0 + 1, 13, 'dark_oak_planks')
    fill(1, F0 + 2, 11, 1, F0 + 3, 13, 'black_concrete')
    sb(1, F0 + 2, 12, 'gray_stained_glass')
    sb(1, F0 + 3, 12, 'light_gray_stained_glass')
    # puerta al jardín (derecha/oeste, x=0, z=9)
    sb(0, F0 + 1, 9, 'spruce_door[facing=west,half=lower,hinge=left]')
    sb(0, F0 + 2, 9, 'spruce_door[facing=west,half=upper,hinge=left]')
    fill(-2, 64, 9, -1, 65, 9, 'cobblestone')
    sb(-1, F0, 9, 'spruce_planks')
    sb(-2, 65, 9, 'spruce_stairs[facing=east]')
    sb(-2, 64, 9, 'cobblestone')
    sb(-3, 64, 9, 'spruce_stairs[facing=east]')
    sb(8, F1 - 1, 11, 'lantern[hanging=true]')
    # ventanas planta baja
    for x in (3, 13):
        fill(x - 1, F0 + 2, 0, x, F0 + 3, 0, 'glass_pane')
    for z in (3, 12):
        fill(0, F0 + 2, z, 0, F0 + 3, z + 1, 'glass_pane')
        fill(16, F0 + 2, z, 16, F0 + 3, z + 1, 'glass_pane')
    fill(4, F0 + 2, 15, 6, F0 + 3, 15, 'glass_pane')
    fill(10, F0 + 2, 15, 12, F0 + 3, 15, 'glass_pane')
    # ---- segundo piso: pasillo x6..10 z1..8; cuarto derecha (oeste) x1..5,
    # cuarto izquierda (este) x11..15, cuarto de frente x6..10 z10..14
    fill(5, F1 + 1, 1, 5, F1 + 4, 14, 'birch_planks')
    fill(11, F1 + 1, 1, 11, F1 + 4, 14, 'birch_planks')
    fill(6, F1 + 1, 9, 10, F1 + 4, 9, 'birch_planks')
    for (x, z, f) in ((5, 7, 'west'), (11, 7, 'east'), (8, 9, 'south')):
        sb(x, F1 + 1, z, f'spruce_door[facing={f},half=lower,hinge=left]')
        sb(x, F1 + 2, z, f'spruce_door[facing={f},half=upper,hinge=left]')
    # cuarto de Juli (derecha)
    sb(2, F1 + 1, 12, 'pink_bed[facing=south,part=foot]')
    sb(2, F1 + 1, 13, 'pink_bed[facing=south,part=head]')
    fill(1, F1, 10, 4, F1, 14, 'pink_carpet') if False else None
    fill(1, F1 + 1, 9, 4, F1 + 1, 11, 'pink_carpet')
    sb(4, F1 + 1, 14, 'chest[facing=north]')
    sb(1, F1 + 1, 2, 'spruce_stairs[facing=south]')
    sb(1, F1 + 1, 3, 'spruce_trapdoor[half=top]')
    sb(3, F1 + 1, 1, 'potted_pink_tulip')
    sb(3, F1 + 4, 7, 'lantern[hanging=true]')
    sb(4, F1 + 1, 5, 'candle[candles=2,lit=true]')
    # cuarto izquierda
    sb(14, F1 + 1, 3, 'light_blue_bed[facing=north,part=head]')
    sb(14, F1 + 1, 4, 'light_blue_bed[facing=north,part=foot]')
    fill(15, F1 + 1, 10, 15, F1 + 3, 13, 'bookshelf')
    sb(13, F1 + 4, 8, 'lantern[hanging=true]')
    sb(12, F1 + 1, 14, 'armor_stand') if False else None
    # cuarto de frente
    sb(8, F1 + 1, 14, 'cauldron')
    sb(6, F1 + 1, 14, 'barrel[facing=up]')
    sb(10, F1 + 1, 13, 'white_carpet')
    sb(8, F1 + 4, 12, 'lantern[hanging=true]')
    sb(8, F1 + 4, 4, 'lantern[hanging=true]')
    # ventanas del segundo piso
    for x in (3, 13):
        fill(x - 1, F1 + 2, 0, x, F1 + 3, 0, 'glass_pane')
    for z in (3, 11):
        fill(0, F1 + 2, z, 0, F1 + 3, z + 1, 'glass_pane')
        fill(16, F1 + 2, z, 16, F1 + 3, z + 1, 'glass_pane')
    fill(7, F1 + 2, 15, 9, F1 + 3, 15, 'glass_pane')
    # ---- techo a dos aguas (cumbrera a lo largo de x), aleros
    top = F1 + 4
    for k in range(9):
        y = top + 1 + k
        zf, zb = -1 + k, 16 - k
        if zf > zb:
            break
        fill(-1, y, zf, 17, y, zf, 'dark_oak_stairs[facing=south]')
        fill(-1, y, zb, 17, y, zb, 'dark_oak_stairs[facing=north]')
        if zb - zf >= 2:
            fill(0, y, zf + 1, 0, y, zb - 1, 'birch_planks')
            fill(16, y, zf + 1, 16, y, zb - 1, 'birch_planks')
        if zf == zb or zb - zf == 1:
            fill(-1, y, zf, 17, y, zb, 'dark_oak_slab[type=bottom]' if zf == zb else 'dark_oak_planks')
    fill(1, top + 1, 1, 15, top + 1, 14, 'spruce_planks')
    # dos ventanas en el techo (frente): trampillas que se abren y cierran
    for x in (4, 12):
        sb(x, top + 3, 1, 'spruce_trapdoor[facing=north,half=bottom,open=false]')
        sb(x, top + 3, 2, 'glass')
    # cerca del jardín y árbol
    fill(-12, 64, 5, -12, 64, 21, 'spruce_fence')
    fill(-12, 64, 21, -1, 64, 21, 'spruce_fence')
    fill(-9, 64, 14, -9, 68, 14, 'oak_log')
    fill(-11, 68, 12, -7, 70, 16, 'flowering_azalea_leaves[persistent=true]')
    sb(-9, 69, 14, 'oak_log')
    for (x, z, f) in ((-5, 8, 'poppy'), (-6, 12, 'cornflower'), (-4, 17, 'oxeye_daisy'), (-8, 18, 'allium'), (-10, 9, 'azure_bluet'), (-3, 13, 'pink_tulip')):
        sb(x, 64, z, f)
    sb(-6, 64, 16, 'white_bed[facing=east,part=foot]') if False else None
    B = [b for b in B if b]
    F('casa/build_place', '\n'.join(['execute in canon:sueno_blanco run ' + b for b in B]) + '''
execute in canon:sueno_blanco run function canon:casa/rooms
scoreboard players set #casa_built dv.build 2
execute in canon:sueno_blanco run forceload remove -16 -16 31 31
''')
    F('casa/build_start', '''
scoreboard players set #casa_built dv.build 1
execute in canon:sueno_blanco run forceload add -16 -16 31 31
''')
    F('casa/build_try', 'execute in canon:sueno_blanco if loaded -14 64 -10 if loaded 24 64 26 if loaded -14 64 26 if loaded 24 64 -10 run function canon:casa/build_place')
    rooms = [(3, 67, 4), (13, 67, 3), (12, 67, 12), (-6, 64, 12), (3, 72, 9), (13, 72, 7), (8, 72, 12), (8, 67, 4)]
    lines = ['kill @e[type=marker,tag=dv_jroom]']
    for i, (x, y, z) in enumerate(rooms):
        lines.append(f'summon minecraft:marker {x}.5 {y} {z}.5 {{Tags:["dv_jroom","dv_jroom{i}"]}}')
    F('casa/rooms', '\n'.join(lines))

    # entrar / salir
    F('casa/sleeping', '''
scoreboard players add @s dv.kz 1
execute if score @s dv.kz matches 60 unless entity @s[tag=dv_santi] unless score @s dv.par matches 1.. unless score @s dv.sb matches 1.. if predicate canon:azar/1en2 run function canon:casa/enter
''')
    F('casa/enter', f'''
function canon:travel/store_return
scoreboard players set @s dv.sb 6000
scoreboard players set @s dv.mus 0
scoreboard players set @s dv.kz 0
execute in canon:sueno_blanco run tp @s 12.5 64 -12.5 0 5
effect give @s minecraft:blindness 2 0 true
title @s times 20 70 30
title @s subtitle {jt('Todo es blanco. Menos la casa.', '#cfcfcf', True)}
title @s title {jt('LA CASA', '#ffffff')}
playsound canon:fx.whoosh_white master @s ~ ~ ~ 1 1
execute if score #casa_built dv.build matches 0 run function canon:casa/build_start
tellraw @s {jt('(Estás soñando. Juli está en algún lugar de la casa. Si te alejas mucho, despiertas.)', 'gray', True)}
''')
    F('casa/player', f'''
scoreboard players remove @s[scores={{dv.sb=1..}}] dv.sb 1
execute if score @s dv.mus matches ..0 run function canon:casa/music
execute if score @s dv.sb matches 1200 run title @s actionbar {jt('La casa empieza a desdibujarse...', '#cfcfcf', True)}
execute if score @s dv.sb matches ..0 run function canon:casa/wake
execute unless entity @s[x=-40,y=0,z=-40,dx=96,dy=200,dz=96] run function canon:casa/lost
execute if entity @s[y=-64,dy=60] run function canon:casa/wake
execute if score #m200 dv.clock matches 0 run function canon:casa/ensure_juli
''')
    F('casa/music', '''
scoreboard players set @s dv.mus 1380
playsound canon:music.casa_blanca music @s ~ ~ ~ 0.8 1
playsound canon:sueno.blanco ambient @s ~ ~ ~ 0.6 1
''')
    F('casa/lost', f'''
tellraw @s {jt('Te alejaste de la casa. El blanco te traga.', '#cfcfcf', True)}
function canon:casa/wake
''')
    F('casa/wake', f'''
scoreboard players set @s dv.sb 0
stopsound @s music canon:music.casa_blanca
title @s times 0 10 40
title @s subtitle ""
title @s title ["",{{"text":"\\ue104","font":"canon:susto","color":"white"}}]
function canon:util/tp_return
playsound canon:fx.wake_gasp player @s ~ ~ ~ 1 1
tellraw @s {jt('Despiertas. Soñaste con una casa de madera y con Juli. No recuerdas qué te dijo.', '#f2a7c3', True)}
''')
    F('casa/ensure_juli', '''
execute if score #casa_built dv.build matches 2 in canon:sueno_blanco unless entity @e[type=zombie,tag=dv_jcasa,x=8,y=70,z=8,distance=..80] run function canon:casa/spawn_juli
''')
    F('casa/spawn_juli', '''
execute in canon:sueno_blanco positioned 3.5 67 4.5 run function canon:casa/spawn_juli2
''')
    F('casa/spawn_juli2', '''
scoreboard players set #pid dv.tmp 0
scoreboard players set #jstate dv.tmp 6
function canon:spawn/juli
tag @e[type=zombie,tag=dv_juli,distance=..2,limit=1,sort=nearest] add dv_jcasa
scoreboard players set #jroom dv.dev 0
''')
    # Juli en la casa
    F('casa/juli_tick', '''
tag @a remove dv_jtgt
tag @a[predicate=canon:en_casa_sueno,distance=..8,limit=1,sort=nearest] add dv_jtgt
execute unless entity @a[predicate=canon:en_casa_sueno] run function canon:rig/despawn
execute if entity @a[tag=dv_jtgt] if score #m4 dv.clock matches 0 run function canon:juli/face
execute if entity @a[tag=dv_jtgt,distance=2.5..] if entity @a[tag=dv_jtgt,distance=..5] run function canon:juli/walk_to
scoreboard players add @s dv.timer2 1
execute if score @s dv.timer2 matches 500.. unless entity @a[tag=dv_jtgt,distance=..4] run function canon:casa/move
execute if score @s dv.timer2 matches 900.. run function canon:casa/move
execute if score #m200 dv.clock matches 50 if entity @a[tag=dv_jtgt] if score @s dv.say matches ..0 if predicate canon:azar/1en2 run function canon:casa/idle_line
execute if score #m200 dv.clock matches 100 run function canon:casa/windows
execute if score #m200 dv.clock matches 150 unless entity @a[tag=dv_jtgt] if predicate canon:azar/1en3 run playsound canon:sueno.blanco_eco ambient @a[predicate=canon:en_casa_sueno,distance=..40] ~ ~ ~ 0.6 1
''')
    F('casa/windows', '''
scoreboard players add #win dv.dev 1
scoreboard players operation #c dv.tmp = #win dv.dev
scoreboard players operation #c dv.tmp %= #2 dv.math
execute if score #c dv.tmp matches 0 run setblock 4 78 1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=false]
execute if score #c dv.tmp matches 0 run setblock 12 78 1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=false]
execute if score #c dv.tmp matches 1 run setblock 4 78 1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=true]
execute if score #c dv.tmp matches 1 run setblock 12 78 1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=true]
playsound minecraft:block.wooden_trapdoor.open block @a[distance=..40] 8 78 1 0.6 0.8
''')
    F('casa/move', '''
scoreboard players set @s dv.timer2 0
particle minecraft:cherry_leaves ~ ~1 ~ 0.4 0.9 0.4 0 25 normal
particle minecraft:end_rod ~ ~1 ~ 0.3 0.7 0.3 0.02 8 normal
scoreboard players set #r dv.tmp 0
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 2
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 4
execute if score #r dv.tmp = #jroom dv.dev run scoreboard players add #r dv.tmp 3
scoreboard players operation #r dv.tmp %= #8 dv.math
scoreboard players operation #jroom dv.dev = #r dv.tmp
''' + '\n'.join(f'execute if score #r dv.tmp matches {i} run tp @s @e[type=marker,tag=dv_jroom{i},limit=1]' for i in range(8)) + '''
execute at @s run particle minecraft:cherry_leaves ~ ~1 ~ 0.4 0.9 0.4 0 25 normal
execute at @s run playsound canon:juli.chime ambient @a[distance=..20] ~ ~ ~ 0.5 1.2
''')
    J = '#ffe3ee'
    jsay = lambda t, ticks=100: bubble('dv_juli_bubble', t, J, ticks) + '\n' + chat('Juli', '#f2a7c3', t, '@a[distance=..10]')
    ROOM_LINES = {
        0: ['Estoy haciendo chocolate caliente. Nunca hierve, pero huele rico.', '¿Viste la nevera? Siempre está llena de cosas que no existen.', 'Aquí cocinaba mi mamá. Bueno, la mamá de la casa.'],
        1: ['Este cuarto siempre está ordenado. Nadie duerme aquí.', 'Los libros están en blanco. Todos. Los he revisado.', 'Si te acuestas en esa cama, sueñas dentro del sueño. No lo hagas.'],
        2: ['La tele solo pasa estática. Pero me gusta el ruido.', 'Siéntate en el sofá. Es el único lugar donde no se oye arriba.', 'A veces la tele dice nombres. El tuyo no. Todavía.'],
        3: ['Aquí afuera no hay nada. Solo blanco. No te alejes de la cerca.', 'Planté flores. Crecen cuando alguien sueña conmigo.', 'El árbol es lo único que tiene sombra. Me gusta.'],
        4: ['Este es mi cuarto. No mires debajo de la cama. Es broma. O no.', '¿Dónde dejé mi collar? Ah, lo tengo puesto. Jaja.', 'Desde la ventana del techo se ve todo blanco. Y a veces algo que camina.'],
        5: ['Estoy buscando una foto vieja. Aquí se pierden las cosas.', 'Alguien deja la ventana abierta. Siempre. Yo la cierro.', 'Este cuarto huele a lluvia. No llueve nunca aquí.'],
        6: ['No sé para qué es este cuarto. Solo sé que hay que cerrarlo de noche.', 'Shh. Escucha. ¿Oyes pasos abajo? Somos nosotros. Creo.', 'Aquí guardo lo que la gente olvida al despertar.'],
        7: ['Bienvenido. Cierra la puerta, que entra el blanco.', 'Las escaleras crujen aunque nadie las pise.', 'Ven, te muestro la casa. O búscame tú.'],
    }
    for i, ls in ROOM_LINES.items():
        pick(f'casa/room_line/r{i}', [jsay(t, 110) for t in ls])
    F('casa/idle_line', '\n'.join(f'execute if score #jroom dv.dev matches {i} run function canon:casa/room_line/r{i}' for i in range(8)))
    F('casa/clicked', f'''
execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound canon:juli.chime ambient @a[distance=..12] ~ ~ ~ 0.4 1.3
scoreboard players set @s dv.timer2 0
{menu('@a[tag=dv_talker]', 'JULI', '#f2a7c3', [
        ('¿Dónde estamos?', '/trigger dv.jr set 1'), ('¿Qué haces?', '/trigger dv.jr set 2'),
        ('¿Estás bien?', '/trigger dv.jr set 3'), ('Me tengo que ir', '/trigger dv.jr set 4')])}
''')
    F('casa/attacked', jsay('Ay. ¿Por qué...? Aquí nadie se hace daño. Solo se olvida.', 90))
    F('casa/choice', '''
tag @s add dv_jtalk
scoreboard players operation #jc dv.tmp = @s dv.jr
scoreboard players set @s dv.jr 0
scoreboard players set #jf dv.tmp 0
execute as @e[type=zombie,tag=dv_jcasa,distance=..14,limit=1,sort=nearest] run scoreboard players set #jf dv.tmp 1
execute if score #jf dv.tmp matches 0 run tellraw @s {"text":"Juli no está cerca.","color":"gray","italic":true}
execute if score #jf dv.tmp matches 1 as @e[type=zombie,tag=dv_jcasa,distance=..14,limit=1,sort=nearest] at @s run function canon:casa/c/run
tag @s remove dv_jtalk
''')
    F('casa/c/run', '\n'.join(f'execute if score #jc dv.tmp matches {i} run function canon:casa/c/c{i}' for i in range(1, 10)) + '\nscoreboard players set @s dv.timer2 0')
    jm = lambda b: menu('@a[tag=dv_jtalk]', '', '#f2a7c3', b)
    F('casa/c/c1', jsay('En la casa. La que sueña la gente que duerme cerca de Santi. No sé por qué, pero siempre termino aquí.', 160) + '\n' +
      jm([('¿Santi?', '/trigger dv.jr set 5'), ('¿Por qué todo es blanco?', '/trigger dv.jr set 6')]))
    F('casa/c/c2', '\n'.join(f'execute if score #jroom dv.dev matches {i} run function canon:casa/room_line/r{i}' for i in range(8)) + '\n' +
      jm([('¿Te ayudo?', '/trigger dv.jr set 7'), ('Sigue tranquila', '/trigger dv.jr set 9')]))
    F('casa/c/c3', jsay('Estoy bien. A veces escucho a alguien caminando arriba, cuando no hay nadie.', 140) + '\n' +
      jm([('Vamos a ver', '/trigger dv.jr set 8'), ('Mejor no', '/trigger dv.jr set 9')]))
    F('casa/c/c4', jsay('Está bien. Cierra los ojos y cuenta hasta tres. Vuelve cuando quieras.', 80) + '\n'
      'execute as @a[tag=dv_jtalk] at @s run function canon:casa/wake')
    F('casa/c/c5', jsay('Santi es alguien importante. Si lo ves, dile que lo espero en el otro sueño, el de las flores.', 160))
    F('casa/c/c6', jsay('Porque la casa es lo único que alguien recuerda bien. Lo demás se borró.', 140))
    F('casa/c/c7', jsay('¿En serio? Perdí una foto vieja. Búscala en el cuarto de arriba a la izquierda. Ahí siempre se pierden las cosas.', 160) + '''
kill @e[type=interaction,tag=dv_cfoto]
kill @e[type=item_display,tag=dv_cfoto_vis]
execute in canon:sueno_blanco run summon minecraft:item_display 14.5 72.3 12.5 {Tags:["dv_cfoto_vis"],brightness:{sky:15,block:15},billboard:"vertical",item:{id:"minecraft:paper",Count:1b},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5f,0.5f,0.5f],right_rotation:[0f,0f,0f,1f]}}
execute in canon:sueno_blanco run summon minecraft:interaction 14.5 72 12.5 {Tags:["dv_cfoto","dv_click","dv_npc_click"],width:0.8f,height:0.8f,response:1b}
''')
    F('casa/c/c8', jsay('Ven. Sígueme... Ves, no hay nadie arriba. ¿O sí?', 120) + '''
tp @s @e[type=marker,tag=dv_jroom6,limit=1]
scoreboard players set #jroom dv.dev 6
scoreboard players set @s dv.timer2 0
playsound canon:sueno.blanco_eco ambient @a[tag=dv_jtalk] ~ ~ ~ 1 0.8
schedule function canon:casa/upstairs_scare 100t replace
''')
    F('casa/upstairs_scare', '''
execute if score #miron dv.cfg matches 1 in canon:sueno_blanco unless entity @e[type=zombie,tag=dv_miron,x=8,y=72,z=8,distance=..30] positioned 8.5 72 2.5 if entity @a[distance=..12] run function canon:miron/spawn_here
execute in canon:sueno_blanco positioned 8.5 72 2.5 run playsound canon:miron.respira hostile @a[distance=..16] ~ ~ ~ 1 0.8
''')
    F('casa/c/c9', jsay('Tienes razón. Quedémonos aquí un rato. Así está bien.', 90))
    F('casa/foto_taken', '''
kill @e[type=item_display,tag=dv_cfoto_vis]
tellraw @a[tag=dv_talker] {"text":"Es una foto de Juli riéndose en un parque. Atrás alguien escribió: «no me olvides».","color":"#f2a7c3","italic":true}
loot give @a[tag=dv_talker] loot canon:items/petalo
playsound canon:juli.chime ambient @a[tag=dv_talker] ~ ~ ~ 0.8 1
execute as @e[type=zombie,tag=dv_jcasa,limit=1] at @s run function canon:casa/thanks
kill @s
''')
    F('casa/thanks', jsay('¡La encontraste! Gracias. Toma un pétalo. Te va a proteger cuando despiertes.', 130))


# =================================================================== PUEBLO

def gen_town():
    pick('town2/event', [
        'execute positioned ^ ^ ^18 run function canon:miron/try',
        'playsound canon:furniture.phone_ring ambient @s ^8 ^ ^-6 0.8 1\ntellraw @s ' + jt('Suena un teléfono en una casa vacía.', 'gray', True),
        'effect give @s minecraft:darkness 4 0 true\nplaysound canon:fx.blackout ambient @s ~ ~ ~ 0.7 1\ntellraw @s ' + jt('Las luces del pueblo parpadean y se apagan un segundo.', 'gray', True),
        'playsound canon:devota.whisper ambient @s ^ ^ ^-2 0.7 0.8',
        'function canon:town2/stare',
        'execute if score #nicolas dv.cfg matches 1 run playsound canon:nicolas.risa ambient @s ^-10 ^2 ^8 0.7 1\nexecute if score #nicolas dv.cfg matches 1 run tellraw @s ' + jt('Una risa sale de una casa cerrada.', 'gray', True),
        'playsound canon:animals.crow ambient @s ^ ^6 ^ 1 0.8\nparticle minecraft:large_smoke ^ ^8 ^6 3 1 3 0.01 20 normal @s',
    ])
    F('town2/stare', '''
tag @s add dv_stared
execute as @e[type=wandering_trader,tag=dv_brain,distance=..32] at @s run tp @s ~ ~ ~ facing entity @a[tag=dv_stared,limit=1] eyes
execute if entity @e[type=wandering_trader,tag=dv_brain,distance=..32] run tellraw @s {"text":"Todos en la calle se detienen. Todos te miran.","color":"#c94a4a","italic":true}
tag @s remove dv_stared
''')


# =================================================================== ADMIN / CONFIG

def gen_admin():
    F('admin/config/miron', '''
execute if score #miron dv.cfg matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score #miron dv.cfg matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation #miron dv.cfg = #tg dv.tmp
function canon:admin/config
''')
    F('admin/spawn/kevin', 'execute positioned ^ ^ ^2 run function canon:kevin/summon\nexecute as @e[type=zombie,tag=dv_kevin,distance=..4,limit=1,sort=nearest] at @s run function canon:kevin/greet')
    F('admin/spawn/nicolas', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^6 run function canon:nicolas/summon')
    F('admin/spawn/miron', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^12 run function canon:miron/spawn_here')
    F('admin/kevin/fiesta', 'execute as @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] at @s run function canon:kevin/fiesta/start')
    F('admin/kevin/bosque', 'tag @s add dv_ktalk\nexecute as @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] at @s run function canon:kevin/bosque/start\ntag @s remove dv_ktalk')
    F('admin/kevin/catacumbas', 'tag @s add dv_ktalk\nexecute as @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] at @s run function canon:kevin/cata/prep\ntag @s remove dv_ktalk')
    F('admin/kevin/tres_dias', 'execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn\nfunction canon:kevin/dias/begin\ntellraw @s {"text":"[Canon Event] Empiezan los 3 días sin Kevin.","color":"dark_gray"}')
    F('admin/kevin/volver', 'function canon:kevin/dias/return')
    F('admin/kevin/parar', 'function canon:kevin/ev/abort\ntellraw @s {"text":"[Canon Event] Evento de Kevin detenido.","color":"dark_gray"}')
    F('admin/kevin/reiniciar', 'scoreboard players set #kprog dv.dev 1\nscoreboard players set #kdays dv.dev 0\ntellraw @s {"text":"[Canon Event] Historia de Kevin reiniciada (fiesta disponible).","color":"dark_gray"}')
    F('admin/ir_a_la_casa', 'function canon:casa/enter')
    F('admin/susto_mina', 'function canon:nicolas/face_scare')
    cmds = [('/function canon:admin/spawn/kevin', 'Traer a Kevin'),
            ('/function canon:admin/kevin/fiesta', 'Kevin: empezar la fiesta'),
            ('/function canon:admin/kevin/bosque', 'Kevin: empezar el bosque'),
            ('/function canon:admin/kevin/catacumbas', 'Kevin: bajar a las catacumbas'),
            ('/function canon:admin/kevin/tres_dias', 'Kevin: empezar los 3 días'),
            ('/function canon:admin/kevin/volver', 'Kevin: terminar los 3 días'),
            ('/function canon:admin/kevin/parar', 'Detener el evento de Kevin'),
            ('/function canon:admin/kevin/reiniciar', 'Reiniciar la historia de Kevin'),
            ('/function canon:admin/spawn/nicolas', 'Traer a Nicolás'),
            ('/function canon:admin/susto_mina', 'Probar el susto de la mina'),
            ('/function canon:admin/spawn/miron', 'Traer al Mirón'),
            ('/function canon:admin/ir_a_la_casa', 'Soñar con la casa de Juli')]
    parts = ['""', jt('\nCOMANDOS NUEVOS\n', '#ffb347')]
    for c, d in cmds:
        parts.append(json.dumps({'text': c, 'color': '#e8c9a8', 'clickEvent': {'action': 'suggest_command', 'value': c}}, ensure_ascii=False))
        parts.append(jt('  ' + d + '\n', 'dark_gray'))
    F('menu/commands2', 'tellraw @s [' + ','.join(parts) + ']')


def gen_predicates():
    biomes = ['forest', 'flower_forest', 'birch_forest', 'dark_forest', 'old_growth_birch_forest', 'old_growth_pine_taiga',
              'old_growth_spruce_taiga', 'taiga', 'snowy_taiga', 'jungle', 'sparse_jungle', 'bamboo_jungle', 'windswept_forest',
              'cherry_grove', 'mangrove_swamp', 'grove', 'swamp']
    p = {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:location_check', 'predicate': {'biome': 'minecraft:' + b}} for b in biomes]}
    json.dump(p, open(os.path.join(DATA, 'predicates', 'en_bosque.json'), 'w'), indent=2)
    json.dump({'condition': 'minecraft:location_check', 'predicate': {'dimension': 'canon:sueno_blanco'}},
              open(os.path.join(DATA, 'predicates', 'en_casa_sueno.json'), 'w'), indent=2)


def gen_luna():
    F('luna/n/nicolas', '''
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_luna_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¡Ese chico de negro huele a rabia! ¡Grrr! ¡Corre!","color":"#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 60
function canon:luna/bark2
scoreboard players set @s dv.talkcd 600
''')


# =================================================================== PARCHES a archivos existentes

def patch(path, fn):
    p = os.path.join(FN, path + '.mcfunction')
    s = open(p).read()
    s2 = fn(s)
    if s2 != s:
        FILES[path] = s2


def gen_patches():
    patch('load', lambda s: s if 'canon:extra/load' in s else s.replace('tellraw @a[scores={dv.debug=1}]', 'function canon:extra/load\ntellraw @a[scores={dv.debug=1}]'))
    patch('tick', lambda s: s if 'canon:extra/tick' in s else s.rstrip('\n') + '\nfunction canon:extra/tick\n')
    patch('rig/die', lambda s: s if 'nicolas/died' in s else s.rstrip('\n') + '\nexecute if entity @s[tag=dv_nicolas] run function canon:nicolas/died\n')
    patch('juli/tick', lambda s: s if 'casa/juli_tick' in s else s.replace(
        'execute if score @s dv.state matches 5 run function canon:juli/s_bye',
        'execute if score @s dv.state matches 5 run function canon:juli/s_bye\nexecute if score @s dv.state matches 6 run function canon:casa/juli_tick'))
    # clic / golpe sobre la Juli de la casa
    base = os.path.join(FN, 'juli', 'clicked_me_base.mcfunction')
    if not os.path.exists(base):
        FILES['juli/clicked_me_base'] = open(os.path.join(FN, 'juli', 'clicked_me.mcfunction')).read()
        FILES['juli/clicked_me'] = ('execute if entity @s[tag=dv_jcasa] run function canon:casa/clicked\n'
                                    'execute unless entity @s[tag=dv_jcasa] run function canon:juli/clicked_me_base\n')
    hb = os.path.join(FN, 'juli', 'hurt_base.mcfunction')
    if not os.path.exists(hb):
        FILES['juli/hurt_base'] = open(os.path.join(FN, 'juli', 'hurt.mcfunction')).read()
        FILES['juli/hurt'] = ('execute if entity @s[tag=dv_jcasa] run function canon:casa/attacked\n'
                              'execute unless entity @s[tag=dv_jcasa] run function canon:juli/hurt_base\n')
    patch('luna/notice', lambda s: s if 'luna/n/nicolas' in s else s.rstrip('\n') +
          '\nexecute if score @s dv.talkcd matches ..0 if entity @e[type=zombie,tag=dv_nicolas,distance=..16] run function canon:luna/n/nicolas\n')
    # menú de ajustes: agregar el Mirón
    def cfg(s):
        if 'config/miron' in s:
            return s
        entry = (',{"text":"[El Mirón (algo te mira a lo lejos)] ","color":"#e8c9a8","clickEvent":{"action":"run_command","value":"/function canon:admin/config/miron"}},'
                 '{"score":{"name":"#miron","objective":"dv.cfg"},"color":"white"},{"text":"\\n"}]')
        s = s.rstrip('\n')
        assert s.endswith(']')
        return s[:-1] + entry + '\n'
    patch('admin/config', cfg)
    patch('menu/trigger', lambda s: s if 'menu/commands2' in s else s.replace(
        'scoreboard players set @s dv.menu 0',
        'execute if score @s dv.menu matches 5 run function canon:menu/commands2\nscoreboard players set @s dv.menu 0'))


def main():
    register_models()
    gen_hooks()
    gen_kevin()
    gen_fiesta()
    gen_bosque()
    gen_cata()
    gen_dias()
    gen_nicolas()
    gen_miron()
    gen_casa()
    gen_town()
    gen_admin()
    gen_luna()
    gen_patches()
    gen_predicates()
    for path, text in FILES.items():
        p = os.path.join(FN, path + '.mcfunction')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
    print(len(FILES), 'funciones escritas')


if __name__ == '__main__':
    main()
