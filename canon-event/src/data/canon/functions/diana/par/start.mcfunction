tp @s ~ ~ ~
scoreboard players set @s dv.par 1
scoreboard players set @s dv.parcd 12000
effect give @s minecraft:slowness infinite 255 true
effect give @s minecraft:jump_boost infinite 250 true
effect give @s minecraft:resistance infinite 4 true
effect give @s minecraft:mining_fatigue infinite 4 true
stopsound @s music
playsound canon:diana.paralysis master @s ~ ~ ~ 1 1
scoreboard players operation #pid dv.tmp = @s dv.pid
summon minecraft:marker ~ ~ ~ {Tags:["dv_panchor","dv_new_pa"]}
execute as @e[type=marker,tag=dv_new_pa] run scoreboard players operation @s dv.target = #pid dv.tmp
tag @e[tag=dv_new_pa] remove dv_new_pa
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^3 ^ ^ run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-3 ^ ^ run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^ ^ ^-3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^2 ^ ^2 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-2 ^ ^2 run function canon:util/spot_search
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #dstate dv.tmp 4
tag @s add dv_dtgt
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/diana
tag @s remove dv_dtgt
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 0 run function canon:diana/par/release
title @s times 20 400 20
title @s subtitle ""
title @s title ["",{"text":"","font":"canon:susto","color":"white"}]
tellraw @s {"text":"Abres los ojos. No puedes moverte.","color":"gray","italic":true}
