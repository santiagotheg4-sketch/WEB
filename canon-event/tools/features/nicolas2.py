"""Nicolás reconstruido: ahora es un monstruo Java (canonevent:nicolas, Nicolas.java) con su skin en 3D, que busca el camino
de verdad por las cuevas. Cada vez hace algo distinto (acechar y esconderse, colgar del techo y caer, perseguirte,
apagarte las antorchas, picar la pared hasta abrir un hueco y mirarte). Además, más sustos de cueva: letras en la pared
detrás de ti, grava que cae, la roca que respira y risas que hacen eco."""
from canon.shim import *  # noqa: F401,F403
from canon import shim

LETREROS = ['TE VEO', 'SIGUE CAVANDO', 'NO MIRES ATRÁS', 'AQUÍ ABAJO NADIE TE OYE', 'YA CASI', 'ESTOY CONTIGO', 'JAJAJA']


def ojos(path):
    """Los ojos de Nicolás brillan blancos en la oscuridad (calza con la cara de su skin 64x64)."""
    from PIL import Image
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for x in (9, 10, 13, 14):
        im.putpixel((x, 12), (255, 255, 255, 255))
    im.save(path)


def build(c):
    shim.use(c)
    ojos(c.path('assets/canonevent/textures/entity/nicolas_ojos.png'))
    c.text('entity.canonevent.nicolas', 'Nicolás')
    # menos seguido: que no sea todo el tiempo (antes 1 en 120 por segundo)
    c.patch('extra/second', lambda s: s.replace('unless entity @e[tag=dv_nicx,distance=..48] if predicate canon:azar/1en120 run function canon:mej/nico/elegir',
                                                'unless entity @e[tag=dv_nicx,distance=..48] if predicate canon:azar/1en900 run function canon:mej/nico/elegir'))
    hay = '@e[type=canonevent:nicolas,distance=..96]'
    c.patch('nicolas/summon', lambda s: 'summon canonevent:nicolas ~ ~ ~')
    c.patch('nicolas/try', lambda s: s.replace('@e[type=zombie,tag=dv_nicolas,distance=..96]', hay))
    c.patch('mej/nico/techo', lambda s: 'execute rotated ~ 0 positioned ^ ^ ^3 run summon canonevent:nicolas ~ ~ ~ {Tags:["dv_ntecho","dv_nicx"]}')
    c.patch('mej/nico/corre', lambda s: s.replace('run function canon:mej/niccorre/summon', 'run summon canonevent:nicolas ~ ~ ~ {Tags:["dv_ncorre","dv_nicx"]}'))
    c.patch('mej/nico/elegir', lambda s: s)  # sigue eligiendo entre ojos / techo / corre
    # quedan del Nicolás viejo (zombi que atravesaba paredes): se borran
    c.on('second', 'execute as @e[type=zombie,tag=dv_nicolas] at @s run function canon:rig/despawn\n'
                   'execute as @e[type=zombie,tag=dv_nictecho] at @s run function canon:rig/despawn\n'
                   'execute as @e[type=zombie,tag=dv_niccorre] at @s run function canon:rig/despawn')

    # ---------------------------------------------------------------- sustos de cueva
    cueva = '[gamemode=!spectator,gamemode=!creative,predicate=canon:oscuro]'
    c.on('second', f'''
execute if score #nicolas dv.cfg matches 1 as @a{cueva} at @s if entity @s[y=-64,dy=104] unless block ~ ~ ~ minecraft:water if predicate canon:azar/1en700 run function canon:nic2/susto
execute if score #nicolas dv.cfg matches 1 as @a{cueva} at @s if entity @s[y=-64,dy=104] unless entity {hay} if predicate canon:azar/1en900 run function canon:nic2/mas
''')
    c.pick('nic2/susto', ['function canon:nic2/letrero', 'function canon:nic2/grava', 'function canon:nic2/respira', 'function canon:nic2/risa_eco',
                          'function canon:nic2/letrero', 'function canon:nic2/pico'])
    c.pick('nic2/mas', ['execute rotated ~ 0 positioned ^ ^ ^-12 run summon canonevent:nicolas ~ ~ ~ {Tags:["dv_napaga","dv_nicx"]}',
                        'execute rotated ~ 0 positioned ^ ^ ^-3 run summon canonevent:nicolas ~ ~ ~ {Tags:["dv_npica","dv_nicx"]}',
                        'function canon:mej/nico/techo'])
    # letras rojas en la pared, justo detrás de ti
    F('nic2/letrero', '''
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^1.4 ^-1 run function canon:nic2/letrero_buscar
''')
    F('nic2/letrero_buscar', '''
scoreboard players add #ok dv.tmp 1
execute unless block ~ ~ ~ #canon:pasable positioned ^ ^ ^0.52 run function canon:nic2/letrero_poner
execute if score #ok dv.tmp matches 1..5 if block ~ ~ ~ #canon:pasable positioned ^ ^ ^-1 run function canon:nic2/letrero_buscar
''')
    c.pick('nic2/letrero_poner', ['scoreboard players set #ok dv.tmp 99\n'
                                  f'summon minecraft:text_display ~ ~ ~ {{Tags:["dv_nletrero"],text:\'{{"text":"{t}","color":"#8a0b0b","bold":true}}\',background:0,'
                                  'brightness:{sky:8,block:8},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.6f,1.6f,1.6f],right_rotation:[0f,0f,0f,1f]}}\n'
                                  'execute as @e[type=text_display,tag=dv_nletrero,distance=..1] at @s facing entity @p eyes run tp @s ~ ~ ~ ~ 0\n'
                                  'playsound minecraft:block.stone.hit hostile @p ~ ~ ~ 0.8 0.6' for t in LETREROS])
    c.on('second', 'execute as @e[type=text_display,tag=dv_nletrero] at @s run function canon:nic2/letrero_tick')
    F('nic2/letrero_tick', 'scoreboard players add @s dv.timer 1\nexecute if score @s dv.timer matches 40.. run kill @s')
    # grava que cae detrás de ti
    F('nic2/grava', '''
execute rotated ~ 0 positioned ^ ^4 ^-3 if block ~ ~ ~ #canon:pasable run setblock ~ ~ ~ minecraft:gravel
execute rotated ~ 0 positioned ^1 ^4 ^-3 if block ~ ~ ~ #canon:pasable run setblock ~ ~ ~ minecraft:gravel
playsound minecraft:block.gravel.break block @s ^ ^2 ^-3 1 0.6
particle minecraft:ash ^ ^2 ^-3 0.6 1 0.6 0 60 normal @s
title @s actionbar {"text":"Algo se movió en el techo, detrás de ti","color":"#8a8a96","italic":true}
''')
    # la roca respira
    F('nic2/respira', 'playsound canon:gen.respira_lenta hostile @s ^ ^ ^-2 1 0.6\nplaysound canon:gen.latido hostile @s ~ ~ ~ 0.6 0.8\nscoreboard players add @s dv.miedo 4')
    # risas que hacen eco por todos lados
    F('nic2/risa_eco', '''
playsound canon:nicolas.risa hostile @s ^8 ^ ^ 0.6 0.9
schedule function canon:nic2/risa_eco2 20t append
''')
    F('nic2/risa_eco2', 'execute as @a[predicate=canon:oscuro] at @s run playsound canon:nicolas.risa hostile @s ^-8 ^ ^-4 0.4 0.8')
    # un pico picando muy cerca, del otro lado de la pared
    F('nic2/pico', '''
playsound minecraft:block.stone.hit block @s ^2 ^ ^ 1 0.7
playsound minecraft:block.stone.hit block @s ^2 ^ ^ 1 0.75
playsound minecraft:block.stone.break block @s ^2 ^ ^ 0.8 0.6
title @s actionbar {"text":"Alguien pica la piedra, muy cerca","color":"#8a8a96","italic":true}
''')
    for nm, cmd, desc in [('lejos', 'summon canonevent:nicolas ^ ^ ^20 {Tags:["dv_nlejos"]}', 'Nicolás te mira desde lejos con los ojos blancos'),
                          ('acecha', 'summon canonevent:nicolas ^ ^ ^12', 'Nicolás te acecha (se esconde si lo miras)'),
                          ('techo', 'summon canonevent:nicolas ^ ^ ^3 {Tags:["dv_ntecho"]}', 'Nicolás en el techo (cae delante de ti)'),
                          ('corre', 'summon canonevent:nicolas ^ ^ ^10 {Tags:["dv_ncorre"]}', 'Nicolás te persigue'),
                          ('apaga', 'summon canonevent:nicolas ^ ^ ^-10 {Tags:["dv_napaga"]}', 'Nicolás te apaga las antorchas'),
                          ('pica', 'summon canonevent:nicolas ^ ^ ^-3 {Tags:["dv_npica"]}', 'Nicolás golpea la piedra del otro lado de la pared'),
                          ('letrero', 'function canon:nic2/letrero', 'Letras rojas en la pared detrás de ti'),
                          ('grava', 'function canon:nic2/grava', 'Grava que cae detrás de ti')]:
        F(f'admin/nic/{nm}', cmd if cmd.startswith('function') else 'execute rotated ~ 0 run ' + cmd)
        c.admin(f'/function canon:admin/nic/{nm}', desc)
