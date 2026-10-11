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
