function canon:devota/g/second
function canon:luna/g/second
function canon:extra/second
execute as @e[type=marker,tag=dv_mk] at @s if entity @a[distance=..48] run function canon:marker/convert
execute as @e[type=marker,tag=dv_home_mari] at @s run function canon:mariana/home_tick
execute as @e[type=marker,tag=dv_revive] at @s run function canon:gato/revive_tick
execute as @e[tag=dv_brain,type=!horse] run function canon:rig/reinvis
execute as @e[type=zombie,tag=dv_brain] at @s if block ~ ~1.5 ~ minecraft:water run data merge entity @s {InWaterTime:0}
execute as @e[type=interaction,tag=dv_furn_on] at @s run function canon:furn/running
execute as @e[type=interaction,tag=dv_furn_nevera] run function canon:furn/fridge_tick
execute as @a[scores={dv.obs=1..}] at @s as @e[type=interaction,tag=dv_furn_telefono,distance=..14] at @s run function canon:furn/phone_tick
execute as @e[type=armor_stand,tag=dv_seat] unless data entity @s Passengers run kill @s
function canon:town/slow_tick
execute if score #vago dv.cfg matches 1 if score #m200 dv.clock matches 0 as @a[predicate=canon:en_superficie,predicate=canon:de_noche] at @s run function canon:world/vago_chance
