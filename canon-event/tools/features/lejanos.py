"""Apariciones de lejos, también de día: alguien parado a 50 bloques, mirándote. Si lo miras, no se mueve.
Cada vez que le quitas los ojos de encima un rato, está más cerca. Cuando ya está cerca, desaparece... y algo te respira en la nuca.
De día también pueden verse Diana a lo lejos y el Gigante en el horizonte."""
from canon.shim import *  # noqa: F401,F403
from canon import shim

DISTANCIAS = ((1, 36), (2, 26), (3, 18))


def build(c):
    shim.use(c)
    c.config('lejos', 'Apariciones de lejos (también de día)', 1)
    quien = '[gamemode=!spectator,gamemode=!creative,predicate=canon:en_superficie,limit=1,sort=random]'
    c.on('second', f'''
execute if score #lejos dv.cfg matches 1 if predicate canon:de_dia unless entity @e[type=zombie,tag=dv_lejos] as @a{quien} at @s if predicate canon:azar/1en700 run function canon:lej/aparecer
execute if score #lejos dv.cfg matches 1 if predicate canon:de_noche unless entity @e[type=zombie,tag=dv_lejos] as @a{quien} at @s if predicate canon:azar/1en1200 run function canon:lej/aparecer
execute if score #lejos dv.cfg matches 1 if predicate canon:de_dia unless entity @e[type=canonevent:diana] as @a{quien} at @s if predicate canon:azar/1en3000 run function canon:lej/diana
execute if score #lejos dv.cfg matches 1 if predicate canon:de_dia unless entity @e[type=canonevent:gigante] as @a{quien} at @s if entity @s[y=50,dy=300] if predicate canon:azar/1en6000 run function canon:mj/gigante_aparece
''')
    # dónde aparece: lejos, adelante o a un lado (para que lo puedas ver), a veces detrás
    F('lej/aparecer', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
function canon:lej/donde
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:lej/crear
kill @e[type=marker,tag=dv_spot]
''')
    c.pick('lej/donde', [f'execute rotated ~ 0 positioned ^{x} ^ ^{z} run function canon:util/spot_search'
                         for x, z in ((0, 50), (28, 42), (-28, 42), (40, 20), (-40, 20), (0, -48))])
    F('lej/crear', '''
function canon:acecho/elegir_quien
function canon:acecho/aparecer
execute as @e[type=zombie,tag=dv_asomo,tag=!dv_lejos,distance=..3,limit=1,sort=nearest] run function canon:lej/convertir
''')
    F('lej/convertir', '''
tag @s remove dv_asomo
tag @s add dv_lejos
scoreboard players set @s dv.timer 0
scoreboard players set @s dv.watch 0
scoreboard players set @s dv.state 0
scoreboard players set @s dv.mode 0
scoreboard players set @s dv.timer2 0
''')
    c.npc('dv_lejos', 'lej/tick')
    F('lej/tick', '''
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..110] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
execute if entity @a[tag=dv_wtgt] run function canon:lej/piensa
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('lej/piensa', '''
tag @a[tag=dv_wtgt] add dv_lookers
execute if score #m4 dv.clock matches 0 run function canon:x/face
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score #seen dv.tmp matches 1 if score @s dv.watch matches 1 run function canon:lej/primera_vez
execute if score #seen dv.tmp matches 1 run scoreboard players set @s dv.state 1
execute if score #seen dv.tmp matches 1 run scoreboard players set @s dv.timer2 0
execute if score #seen dv.tmp matches 0 if score @s dv.state matches 1 run scoreboard players add @s dv.timer2 1
execute if score @s dv.timer2 matches 30.. run function canon:lej/acerca
execute if entity @a[tag=dv_wtgt,distance=..14] run function canon:lej/fin
execute if score @s dv.timer matches 2400.. run function canon:rig/despawn
''')
    F('lej/primera_vez', '''
title @a[tag=dv_wtgt] actionbar {"text":"Hay alguien parado allá lejos. Mirándote.","color":"#c8a0a0","italic":true}
execute as @a[tag=dv_wtgt] at @s run playsound canon:gen.drone_grave ambient @s ~ ~ ~ 0.5 0.6
scoreboard players add @a[tag=dv_wtgt] dv.miedo 3
''')
    # cada vez que dejas de mirarlo, está más cerca
    F('lej/acerca', 'scoreboard players set @s dv.state 0\nscoreboard players set @s dv.timer2 0\nscoreboard players add @s dv.mode 1\n'
      'execute if score @s dv.mode matches 4.. run function canon:lej/fin\nexecute if score @s dv.mode matches ..3 run function canon:lej/mover')
    F('lej/mover', 'scoreboard players set #ok dv.tmp 0\n' + '\n'.join(
        f'execute if score @s dv.mode matches {m} at @a[tag=dv_wtgt,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^{d} run function canon:util/spot_search'
        for m, d in DISTANCIAS) + '''
execute if score #ok dv.tmp matches 1 run tp @s @e[type=marker,tag=dv_spot,limit=1]
kill @e[type=marker,tag=dv_spot]
execute as @a[tag=dv_wtgt] at @s run playsound canon:miron.estatica hostile @s ~ ~ ~ 0.25 0.5
scoreboard players add @a[tag=dv_wtgt] dv.miedo 4
''')
    F('lej/fin', '''
execute as @a[tag=dv_wtgt] at @s run playsound canon:gen.susurro hostile @s ^ ^ ^-1.2 1 0.8
execute as @a[tag=dv_wtgt] at @s run playsound canon:gen.respira_lenta hostile @s ^ ^ ^-1 0.8 0.9
tellraw @a[tag=dv_wtgt] {"text":"Ya no está. Pero sentiste algo respirándote en la nuca.","color":"#c94a4a","italic":true}
scoreboard players add @a[tag=dv_wtgt] dv.miedo 8
function canon:rig/despawn
''')
    # Diana, de día, a lo lejos (la 3D): se acerca cuando no la miras
    F('lej/diana', 'scoreboard players set #ok dv.tmp 0\nexecute rotated ~ 0 positioned ^ ^ ^44 run function canon:util/spot_search\n'
      'execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run summon canonevent:diana ~ ~ ~\nkill @e[type=marker,tag=dv_spot]')
    F('admin/lej/alguien', 'function canon:lej/aparecer')
    F('admin/lej/diana', 'function canon:lej/diana')
    c.admin('/function canon:admin/lej/alguien', 'Alguien parado a lo lejos (se acerca cuando no lo miras)')
    c.admin('/function canon:admin/lej/diana', 'Diana a lo lejos, de día')
