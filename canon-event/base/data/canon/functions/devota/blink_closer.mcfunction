scoreboard players set @s dv.lose 120
execute if predicate canon:azar/50 run scoreboard players add @s dv.lose 80
scoreboard players set #ok dv.tmp 0
execute as @a[tag=dv_tgt,limit=1] at @s rotated ~ 0 positioned ^4 ^ ^-14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 as @a[tag=dv_tgt,limit=1] at @s rotated ~ 0 positioned ^-5 ^ ^-12 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 run tp @s @e[type=marker,tag=dv_spot,limit=1]
kill @e[type=marker,tag=dv_spot]
execute at @s run function canon:devota/face
