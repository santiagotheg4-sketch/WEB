particle minecraft:large_smoke ~ ~1 ~ 0.2 0.5 0.2 0.01 15 normal
scoreboard players set #ok dv.tmp 0
execute as @a[tag=dv_talker,limit=1] at @s rotated ~180 0 positioned ^ ^ ^11 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 as @a[tag=dv_talker,limit=1] at @s rotated ~ 0 positioned ^ ^ ^10 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 run tp @s @e[type=marker,tag=dv_spot,limit=1]
kill @e[type=marker,tag=dv_spot]
execute at @s run function canon:mariana/turn_away
