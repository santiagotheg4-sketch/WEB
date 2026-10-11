scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^-2.2 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^0.8 ^ ^-2.4 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-0.8 ^ ^-2.4 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^ ^ ^-3.2 run function canon:util/spot_search
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #dstate dv.tmp 2
tag @s add dv_dtgt
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/diana
tag @s remove dv_dtgt
kill @e[type=marker,tag=dv_spot]
