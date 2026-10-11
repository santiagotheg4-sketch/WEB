scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^20 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^6 ^ ^16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^-6 ^ ^14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:miron/spawn_here
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run function canon:miron/announce
