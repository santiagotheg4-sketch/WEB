from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon.models import *  # noqa: F401,F403
import random, json



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



def build(c):
    shim.use(c)
    c.on('second', 'execute as @a[gamemode=!spectator,predicate=canon:en_pueblo] at @s if predicate canon:azar/1en100 run function canon:town2/event')
    gen_town()
