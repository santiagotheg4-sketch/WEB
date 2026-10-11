"""Núcleo: conecta los ganchos del mod base con los módulos y define utilidades x/*.

Utilidades para rigs (ejecutar como el rig, en su posición):
  x/walk, x/walk_slow, x/creep  -> caminar hacia @a[tag=dv_wtgt] (0.16 / 0.12 / 0.07 bloques por tick)
  x/face                         -> mirar a @a[tag=dv_wtgt]
  x/add_bubble                   -> crea burbuja de texto (text_display dv_xbubble) enlazada por dv.id
  x/links_follow                 -> mueve interaction dv_xclick y burbuja dv_xbubble con el rig
  x/bubble_clear                 -> vacía la burbuja
  x/seen                         -> #seen dv.tmp = 1 si algún @a[tag=dv_lookers] mira al rig
Como jugador:
  x/jumpscare, x/blackout
"""
from canon.shim import *  # noqa: F401,F403
from canon import shim


def build(c):
    shim.use(c)
    c.patch('load', lambda s: s if 'canon:extra/load' in s else s.replace(
        'tellraw @a[scores={dv.debug=1}]', 'function canon:extra/load\ntellraw @a[scores={dv.debug=1}]'))
    c.patch('tick', lambda s: s if 'canon:extra/tick' in s else s.rstrip('\n') + '\nfunction canon:extra/tick\n')
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


