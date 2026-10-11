scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^10 ^ ^16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-10 ^ ^16 run function canon:util/spot_search
