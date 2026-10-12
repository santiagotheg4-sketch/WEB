"""Luna: posiciones nuevas y trucos.

Poses nuevas creadas a partir del modelo base de Luna (misma textura): echada, dar la pata,
reverencia de juego, pidiendo (en dos patas), aullar, olfatear, cavar (2). Trucos con menú
(/trigger dv.luna o clic derecho mientras sostienes un palo): sentarse, echarse, dar la pata,
rodar, panza arriba, hacerse la muerta, saltar, reverencia, aullar, pedir, buscar.
También hace poses sola: olfatea, cava, aúlla en luna llena, se echa de noche.
"""
import copy, json, os
from canon.shim import *  # noqa: F401,F403
from canon import shim

LUNA_BODY = 7320104
NEW = ['luna_echada', 'luna_pata', 'luna_reverencia', 'luna_pidiendo', 'luna_aullar', 'luna_olfatear', 'luna_cavar_a', 'luna_cavar_b']
BASE_CMD = 7320700


def frame_of(name):
    return BASE_CMD + NEW.index(name) - LUNA_BODY


def load(c, name):
    return json.load(open(os.path.join(c.out, 'assets', 'canon', 'models', 'modelo', name + '.json')))


def save(c, name, m):
    json.dump(m, open(os.path.join(c.out, 'assets', 'canon', 'models', 'modelo', name + '.json'), 'w'), separators=(',', ':'))


def rot(e, angle, axis, origin):
    e['rotation'] = {'angle': angle, 'axis': axis, 'origin': origin}


def make_models(c):
    idle = load(c, 'luna_idle')
    sit = load(c, 'luna_sit')
    upper = {'body', 'chest', 'neck', 'collar', 'collar_tag', 'head', 'face', 'snout', 'nose', 'ear'}
    headp = {'head', 'face', 'snout', 'nose', 'ear'}
    # echada: todo abajo, patas delanteras estiradas al frente, traseras dobladas
    m = copy.deepcopy(idle)
    for e in m['elements']:
        n = e.get('name', '')
        if n in upper or n.startswith('tail'):
            e['from'][1] -= 4.2
            e['to'][1] -= 4.2
            if 'rotation' in e:
                e['rotation']['origin'][1] -= 4.2
        elif n in ('leg_fr', 'leg_fl'):
            e['from'] = [e['from'][0], 0, 0.6]
            e['to'] = [e['to'][0], 1.0, 5.1]
        elif n in ('leg_br', 'leg_bl'):
            e['from'] = [e['from'][0] - 0.3, 0, 8.6]
            e['to'] = [e['to'][0] + 0.3, 1.6, 12.0]
    save(c, 'luna_echada', m)
    # dar la pata: sentada con la pata delantera derecha al frente
    m = copy.deepcopy(sit)
    for e in m['elements']:
        if e.get('name') == 'sit_front' and e['from'][0] < 8:
            rot(e, 45, 'x', [6.6, 7, 4])
    save(c, 'luna_pata', m)
    # reverencia: frente abajo, cola arriba
    m = copy.deepcopy(idle)
    for e in m['elements']:
        n = e.get('name', '')
        if n in upper:
            rot(e, 22.5, 'x', [8, 4.8, 11])
        elif n in ('leg_fr', 'leg_fl'):
            e['to'][1] = 2.4
        elif n.startswith('tail'):
            rot(e, -45, 'x', [8, 7.4, 11.6])
    save(c, 'luna_reverencia', m)
    # pidiendo: sentada más erguida, patas delanteras dobladas arriba
    m = copy.deepcopy(sit)
    for e in m['elements']:
        n = e.get('name', '')
        if n in upper:
            rot(e, -45, 'x', [8, 4.8, 11])
        elif n == 'sit_front':
            e['from'] = [e['from'][0], 7.5, 1.2]
            e['to'] = [e['to'][0], 8.6, 4.4]
            rot(e, -45, 'x', [8, 4.8, 11])
    save(c, 'luna_pidiendo', m)
    # aullar: sentada con la cabeza hacia arriba
    m = copy.deepcopy(sit)
    for e in m['elements']:
        if e.get('name', '') in headp:
            rot(e, -45, 'x', [8, 8.6, 3.4])
    save(c, 'luna_aullar', m)
    # olfatear: cabeza al suelo
    m = copy.deepcopy(idle)
    for e in m['elements']:
        if e.get('name', '') in headp or e.get('name') in ('neck', 'collar', 'collar_tag'):
            rot(e, 45, 'x', [8, 7.2, 4.4])
    save(c, 'luna_olfatear', m)
    # cavar: reverencia alternando patas delanteras
    for k, (a1, a2) in (('a', (45, -22.5)), ('b', (-22.5, 45))):
        m = copy.deepcopy(idle)
        for e in m['elements']:
            n = e.get('name', '')
            if n in upper:
                rot(e, 22.5, 'x', [8, 4.8, 11])
            elif n == 'leg_fr':
                e['to'][1] = 2.6
                rot(e, a1, 'x', [6.6, 2.6, 4.5])
            elif n == 'leg_fl':
                e['to'][1] = 2.6
                rot(e, a2, 'x', [9.4, 2.6, 4.5])
        save(c, f'luna_cavar_{k}', m)


# trucos: id, nombre, duración (ticks), frame (None = usa display), texto
TRUCOS = [
    (1, 'Sentarse', 60, 9, '¡Sentada! ¿Me gané algo?'),
    (2, 'Echarse', 80, 'luna_echada', 'Me echo. Pero no me duermo, ¿eh?'),
    (3, 'Dar la pata', 60, 'luna_pata', 'Toma mi pata. Es la buena.'),
    (4, 'Rodar', 30, 'luna_echada', '¡Wiii!'),
    (5, 'Panza arriba', 90, 'luna_echada', 'Rascame la panza. Es una orden.'),
    (6, 'Hacerse la muerta', 100, 'luna_echada', '...'),
    (7, 'Saltar', 18, 3, '¡Hop!'),
    (8, 'Reverencia', 60, 'luna_reverencia', '¡Juguemos! ¡Juguemos!'),
    (9, 'Aullar', 70, 'luna_aullar', 'Auuuuuuu.'),
    (10, 'Pedir', 60, 'luna_pidiendo', 'Por favor. Por favor. Por favor.'),
    (11, 'Buscar', 80, 'luna_olfatear', 'Huelo algo... ¡por aquí!'),
]


def build(c):
    shim.use(c)
    for i, n in enumerate(NEW):
        c.model(n, BASE_CMD + i)
    c.after.append(lambda: None)
    make_models(c)
    c.objective('dv.luna', 'trigger')
    for o in ('dv.lpose', 'dv.ltime', 'dv.lty'):
        c.objective(o)
    for n in (2, 8, 20, 60):
        c.const(n)
    c.on('player', 'scoreboard players enable @s dv.luna\nexecute if score @s dv.luna matches 1.. run function canon:luna2/eleccion')
    c.on('tick', 'execute as @e[type=wolf,tag=dv_luna,scores={dv.lpose=1..}] at @s run function canon:luna2/truco_tick')
    c.on('second', '''
execute as @e[type=wolf,tag=dv_luna,tag=!dv_luna_atada] unless score @s dv.lpose matches 1.. at @s run function canon:luna2/sola
''')
    c.patch('rig/frames/luna', lambda s: s if 'luna2/frame' in s else s.rstrip('\n') + '\nexecute if score @s dv.lpose matches 1.. run function canon:luna2/frame\n')
    # frame del truco / pose actual
    fl = []
    for tid, nombre, dur, fr, texto in TRUCOS:
        f = fr if isinstance(fr, int) else frame_of(fr)
        fl.append(f'execute if score @s dv.lpose matches {tid} run scoreboard players set #frame dv.tmp {f}')
    poses_solas = [(20, 'luna_olfatear'), (21, 'luna_cavar_a'), (22, 'luna_aullar'), (23, 'luna_echada')]
    for pid, name in poses_solas:
        fl.append(f'execute if score @s dv.lpose matches {pid} run scoreboard players set #frame dv.tmp {frame_of(name)}')
    fl.append('scoreboard players operation #c dv.tmp = @s dv.ltime')
    fl.append('scoreboard players operation #c dv.tmp %= #8 dv.math')
    fl.append(f'execute if score @s dv.lpose matches 21 if score #c dv.tmp matches 4..7 run scoreboard players set #frame dv.tmp {frame_of("luna_cavar_b")}')
    F('luna2/frame', '\n'.join(fl))
    # menú
    btns = [(n, f'/trigger dv.luna set {tid}') for tid, n, *_ in TRUCOS]
    F('luna2/menu', menu('@s', 'TRUCOS DE LUNA', '#ffd27a', btns))
    c.admin('/trigger dv.luna set 99', 'Menú de trucos de Luna (para todos)')
    F('luna2/eleccion', '''
tag @s add dv_ltalk
scoreboard players operation #lt dv.tmp = @s dv.luna
scoreboard players set @s dv.luna 0
execute if score #lt dv.tmp matches 99 run function canon:luna2/menu
execute unless score #lt dv.tmp matches 99 unless entity @e[type=wolf,tag=dv_luna,distance=..14] run tellraw @s {"text":"Luna no está cerca.","color":"gray","italic":true}
execute unless score #lt dv.tmp matches 99 as @e[type=wolf,tag=dv_luna,distance=..14,limit=1,sort=nearest] at @s run function canon:luna2/truco
tag @s remove dv_ltalk
''')
    lines = ['execute if score @s dv.lpose matches 1.. run function canon:luna2/fin',
             'scoreboard players operation @s dv.lpose = #lt dv.tmp',
             'data merge entity @s {NoAI:1b}',
             'execute facing entity @a[tag=dv_ltalk,limit=1] feet run tp @s ~ ~ ~ ~ 0',
             'execute on passengers if entity @s[tag=dv_body] store result score @s dv.lty run data get entity @s transformation.translation[1] 1000',
             'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 0.8 1.3']
    for tid, nombre, dur, fr, texto in TRUCOS:
        F(f'luna2/dice/t{tid}', f'''
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_luna_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {{text:'{jt(texto, "#ffd27a")}',background:1342177280}}
scoreboard players set @s dv.say 50
''')
        lines.append(f'execute if score #lt dv.tmp matches {tid} run scoreboard players set @s dv.ltime {dur}')
        lines.append(f'execute if score #lt dv.tmp matches {tid} run function canon:luna2/dice/t{tid}')
    lines.append('execute if score #lt dv.tmp matches 5..6 on passengers if entity @s[tag=dv_body] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{left_rotation:[0f,0f,1f,0f]}}')
    lines.append('execute if score #lt dv.tmp matches 9 run playsound minecraft:entity.wolf.howl neutral @a[distance=..32] ~ ~ ~ 1 1.2')
    lines.append('execute if score #lt dv.tmp matches 6 run tellraw @a[tag=dv_ltalk] {"text":"¡Bang! ...Luna se tira al suelo con la lengua afuera. Qué actriz.","color":"#ffd27a","italic":true}')
    F('luna2/truco', '\n'.join(lines))
    F('luna2/truco_tick', '''
scoreboard players remove @s dv.ltime 1
execute if score @s dv.lpose matches 4 if score @s dv.ltime matches 24 on passengers if entity @s[tag=dv_body] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{left_rotation:[0f,0f,0.7071f,0.7071f]}}
execute if score @s dv.lpose matches 4 if score @s dv.ltime matches 18 on passengers if entity @s[tag=dv_body] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{left_rotation:[0f,0f,1f,0f]}}
execute if score @s dv.lpose matches 4 if score @s dv.ltime matches 12 on passengers if entity @s[tag=dv_body] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{left_rotation:[0f,0f,0.7071f,-0.7071f]}}
execute if score @s dv.lpose matches 4 if score @s dv.ltime matches 6 on passengers if entity @s[tag=dv_body] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{left_rotation:[0f,0f,0f,1f]}}
execute if score @s dv.lpose matches 7 if score @s dv.ltime matches 17 on passengers if entity @s[tag=dv_body] run function canon:luna2/salto_arriba
execute if score @s dv.lpose matches 7 if score @s dv.ltime matches 9 on passengers if entity @s[tag=dv_body] run function canon:luna2/salto_abajo
execute if score @s dv.lpose matches 11 if score @s dv.ltime matches 20 run particle minecraft:block minecraft:dirt ~ ~0.2 ~ 0.3 0.1 0.3 0 8 normal
execute if score @s dv.lpose matches 21 if score #m10 dv.clock matches 0 run particle minecraft:block minecraft:dirt ^ ^0.2 ^0.5 0.2 0.1 0.2 0 6 normal
execute if score @s dv.ltime matches ..0 run function canon:luna2/fin
''')
    F('luna2/salto_arriba', '''
execute store result score #ty dv.tmp run data get entity @s transformation.translation[1] 1000
scoreboard players add #ty dv.tmp 900
data merge entity @s {start_interpolation:0,interpolation_duration:7}
execute store result entity @s transformation.translation[1] float 0.001 run scoreboard players get #ty dv.tmp
''')
    F('luna2/salto_abajo', '''
data merge entity @s {start_interpolation:0,interpolation_duration:7}
execute store result entity @s transformation.translation[1] float 0.001 run scoreboard players get @s dv.lty
''')
    F('luna2/fin', '''
scoreboard players set @s dv.lpose 0
scoreboard players set @s dv.ltime 0
data merge entity @s {NoAI:0b}
execute on passengers if entity @s[tag=dv_body] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0f,0f,1f]}}
execute on passengers if entity @s[tag=dv_body] if score @s dv.lty matches -100000..100000 store result entity @s transformation.translation[1] float 0.001 run scoreboard players get @s dv.lty
scoreboard players set @s dv.frame -1
''')
    # poses que hace sola (cuando está tranquila cerca de alguien)
    F('luna2/sola', '''
execute store result score #lday dv.tmp run time query day
scoreboard players operation #lday dv.tmp %= #8 dv.math
execute if predicate canon:de_noche if score #lday dv.tmp matches 0 if predicate canon:azar/1en60 run function canon:luna2/sola/aullar
execute if entity @a[distance=..6] unless entity @e[tag=dv_horror,distance=..24] if predicate canon:azar/1en60 run function canon:luna2/sola/olfatear
execute if entity @a[distance=..6] unless entity @e[tag=dv_horror,distance=..24] if predicate canon:azar/1en100 run function canon:luna2/sola/cavar
execute if predicate canon:de_noche if entity @a[distance=..5] if predicate canon:azar/1en100 run function canon:luna2/sola/echarse
''')
    for name, pid, dur, extra in (('aullar', 22, 70, 'playsound minecraft:entity.wolf.howl neutral @a[distance=..48] ~ ~ ~ 1 1.1'),
                                  ('olfatear', 20, 50, ''), ('cavar', 21, 60, 'playsound minecraft:block.gravel.hit neutral @a[distance=..12] ~ ~ ~ 0.6 1'),
                                  ('echarse', 23, 200, '')):
        F(f'luna2/sola/{name}', f'''
scoreboard players set @s dv.lpose {pid}
scoreboard players set @s dv.ltime {dur}
data merge entity @s {{NoAI:1b}}
execute on passengers if entity @s[tag=dv_body] store result score @s dv.lty run data get entity @s transformation.translation[1] 1000
{extra}
''')
    # clic con hueso en la mano -> menú de trucos
    c.patch('luna/clicked_me', lambda s: s if 'luna2/menu_clic' in s else
            'execute if entity @a[tag=dv_talker,limit=1,nbt={SelectedItem:{id:"minecraft:stick"}}] run function canon:luna2/menu_clic\n'
            'execute unless entity @a[tag=dv_talker,limit=1,nbt={SelectedItem:{id:"minecraft:stick"}}] run function canon:luna2/clic_normal\n')
    F('luna2/clic_normal', c.read_base('luna/clicked_me'))
    F('luna2/menu_clic', 'execute as @a[tag=dv_talker,limit=1] run function canon:luna2/menu')
    c.text('canon.luna.trucos', 'Trucos de Luna')
