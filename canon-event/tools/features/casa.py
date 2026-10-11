from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon.models import *  # noqa: F401,F403
import random, json



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



def build(c):
    shim.use(c)
    c.objective('dv.jr', 'trigger')
    c.objective('dv.kz')
    c.objective('dv.sb')
    c.objective('dv.mus')
    for n in (2, 8):
        c.const(n)
    c.json('data/canon/predicates/en_casa_sueno.json', {'condition': 'minecraft:location_check', 'predicate': {'dimension': 'canon:sueno_blanco'}})
    c.on('load', '''
execute unless score #casa_built dv.build matches 0.. run scoreboard players set #casa_built dv.build 0
execute unless score #jroom dv.dev matches -999999..999999 run scoreboard players set #jroom dv.dev 0
''')
    c.on('player', '''
scoreboard players enable @s dv.jr
execute if score @s dv.jr matches 1.. run function canon:casa/choice
execute if score #suenos dv.cfg matches 1 if data entity @s SleepingX run function canon:casa/sleeping
execute if score @s dv.kz matches 1.. unless data entity @s SleepingX run scoreboard players set @s dv.kz 0
execute if predicate canon:en_casa_sueno run function canon:casa/player
execute if score @s dv.sb matches 1.. unless predicate canon:en_casa_sueno run scoreboard players set @s dv.sb 0
scoreboard players remove @s[scores={dv.mus=1..}] dv.mus 1
''')
    c.on('tick', 'execute if score #casa_built dv.build matches 1 run function canon:casa/build_try')
    c.click('dv_cfoto', 'casa/foto_taken')
    # Juli de la casa: estado 6 y clic/golpe propios
    c.patch('juli/tick', lambda s: s if 'casa/juli_tick' in s else s.replace(
        'execute if score @s dv.state matches 5 run function canon:juli/s_bye',
        'execute if score @s dv.state matches 5 run function canon:juli/s_bye\nexecute if score @s dv.state matches 6 run function canon:casa/juli_tick'))
    F('juli/clicked_me_base', c.read_base('juli/clicked_me'))
    F('juli/hurt_base', c.read_base('juli/hurt'))
    c.patch('juli/clicked_me', lambda s: s if 'casa/clicked' in s else
            'execute if entity @s[tag=dv_jcasa] run function canon:casa/clicked\nexecute unless entity @s[tag=dv_jcasa] run function canon:juli/clicked_me_base\n')
    c.patch('juli/hurt', lambda s: s if 'casa/attacked' in s else
            'execute if entity @s[tag=dv_jcasa] run function canon:casa/attacked\nexecute unless entity @s[tag=dv_jcasa] run function canon:juli/hurt_base\n')
    gen_casa()
    c.admin('/function canon:admin/ir_a_la_casa', 'Soñar con la casa de Juli')
    F('admin/ir_a_la_casa', 'function canon:casa/enter')
