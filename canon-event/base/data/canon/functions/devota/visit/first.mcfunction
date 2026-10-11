scoreboard players set #es dv.tmp 1
scoreboard players set #visit dv.tmp 600
scoreboard players set #dmode dv.tmp 7
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^4 ^ ^20 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-4 ^ ^18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^ ^ ^16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^8 ^ ^14 run function canon:util/spot_search
scoreboard players operation #pid dv.tmp = @s dv.pid
tag @s add dv_tgt
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/devota
tag @s remove dv_tgt
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run function canon:devota/g/met
