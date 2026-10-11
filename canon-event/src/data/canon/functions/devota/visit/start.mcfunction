function canon:devota/g/es
execute if score #es dv.tmp matches 1 run scoreboard players set #visit dv.tmp 1600
execute if score #es dv.tmp matches 2 run scoreboard players set #visit dv.tmp 4800
execute if score #es dv.tmp matches 3 run scoreboard players set #visit dv.tmp 7200
execute if score #es dv.tmp matches 4 run scoreboard players set #visit dv.tmp 9600
execute if score #es dv.tmp matches 5 run scoreboard players set #visit dv.tmp 12000
execute if score #es dv.tmp matches 6 run scoreboard players set #visit dv.tmp 999999
scoreboard players set #dmode dv.tmp 0
execute if score #es dv.tmp matches 1 run scoreboard players set #dmode dv.tmp 2
execute if score #es dv.tmp matches 5 run scoreboard players set #dmode dv.tmp 4
execute if score #es dv.tmp matches 6 run scoreboard players set #dmode dv.tmp 4
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^-20 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^14 ^ ^-16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-14 ^ ^-16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^18 ^ ^ run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-18 ^ ^ run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^ ^ ^-12 run function canon:util/spot_search
execute if score #es dv.tmp matches 1 if score #ok dv.tmp matches 0 run function canon:util/spot_search_front
scoreboard players operation #pid dv.tmp = @s dv.pid
tag @s add dv_tgt
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/devota
tag @s remove dv_tgt
kill @e[type=marker,tag=dv_spot]
