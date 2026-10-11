scoreboard players set #ok dv.tmp 0
execute as @a[tag=dv_dtgt,limit=1] at @s rotated ~ 0 positioned ^ ^ ^-2.2 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 run tp @s @e[type=marker,tag=dv_spot,limit=1]
kill @e[type=marker,tag=dv_spot]
execute at @s run function canon:diana/face
