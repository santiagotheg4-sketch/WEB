scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^-22 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^14 ^ ^-16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-14 ^ ^-16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^18 ^ ^0 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-18 ^ ^0 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^ ^ ^-12 run function canon:util/spot_search
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #jstate dv.tmp 2
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/juli
execute if score #ok dv.tmp matches 1 as @e[type=zombie,tag=dv_juli,distance=..40] if score @s dv.target = #pid dv.tmp at @s facing entity @p feet run tp @s ~ ~ ~ ~ 0
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run playsound canon:juli.chime ambient @s ~ ~ ~ 0.4 0.8
