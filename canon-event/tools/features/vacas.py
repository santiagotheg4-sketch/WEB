"""Vacas raras: de noche una vaca se queda quieta mirándote con ojos rojos; cuando le das la espalda camina hacia ti,
y si la miras se congela otra vez. Si te alcanza, muge con voz humana y vuelve a ser vaca."""
from canon.shim import *  # noqa: F401,F403
from canon import shim


def build(c):
    shim.use(c)
    c.on('second', '''
execute if score #sustos dv.cfg matches 1 if predicate canon:de_noche unless entity @e[tag=dv_vrara] as @a[gamemode=!spectator,gamemode=!creative,limit=1,sort=random] at @s as @e[type=cow,distance=6..24,limit=1,sort=random] if predicate canon:azar/1en240 run function canon:vaca/empieza
''')
    c.on('tick', 'execute as @e[type=cow,tag=dv_vrara] at @s run function canon:vaca/tick')
    F('vaca/empieza', 'tag @s add dv_vrara\nscoreboard players set @s dv.timer 0\ndata merge entity @s {NoAI:1b,Silent:1b}\n'
      'execute as @a[distance=..24,limit=1,sort=nearest] run tellraw @s {"text":"Una vaca dejó de comer. Te está mirando.","color":"gray","italic":true}')
    F('vaca/tick', '''
scoreboard players add @s dv.timer 1
tag @a remove dv_lookers
tag @a[distance=..32,gamemode=!spectator,limit=1,sort=nearest] add dv_lookers
execute facing entity @a[tag=dv_lookers,limit=1] eyes run tp @s ~ ~ ~ ~ ~
function canon:x/seen
execute if score #m10 dv.clock matches 0 anchored eyes run particle minecraft:dust 1 0 0 0.6 ^ ^ ^0.6 0.08 0.02 0.08 0 4 normal
execute if score #seen dv.tmp matches 0 if entity @a[tag=dv_lookers,distance=2..] facing entity @a[tag=dv_lookers,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.09 if block ~ ~ ~ #canon:pasable run tp @s ~ ~ ~
execute if score #seen dv.tmp matches 0 if score #m10 dv.clock matches 0 run playsound minecraft:block.grass.step neutral @a[tag=dv_lookers] ~ ~ ~ 0.4 0.6
execute if entity @a[tag=dv_lookers,distance=..1.8] run function canon:vaca/fin
execute if score @s dv.timer matches 1800.. run function canon:vaca/fin
tag @a remove dv_lookers
''')
    F('vaca/fin', '''
playsound canon:gen.voz_contigo hostile @a[distance=..12] ~ ~ ~ 1 0.6
playsound minecraft:entity.cow.ambient neutral @a[distance=..12] ~ ~ ~ 1 0.4
execute as @a[distance=..3] at @s run function canon:x/jumpscare
tag @s remove dv_vrara
data merge entity @s {NoAI:0b,Silent:0b}
''')
    F('admin/vaca', 'execute as @e[type=cow,distance=..32,limit=1,sort=nearest] run function canon:vaca/empieza')
    c.admin('/function canon:admin/vaca', 'Una vaca rara te mira y se acerca cuando no la miras')
