scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^9 ^ ^34 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-11 ^ ^30 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^ ^ ^26 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^14 ^ ^22 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-6 ^ ^18 run function canon:util/spot_search
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #dstate dv.tmp 1
tag @s add dv_dtgt
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/diana
tag @s remove dv_dtgt
kill @e[type=marker,tag=dv_spot]
