scoreboard players set #ok dv.tmp 0
execute as @a[tag=dv_tgt,limit=1] at @s rotated ~ 0 positioned ^ ^ ^-4.5 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 run tp @s @e[type=marker,tag=dv_spot,limit=1]
kill @e[type=marker,tag=dv_spot]
execute at @s run function canon:devota/face
playsound canon:devota.whisper hostile @a[tag=dv_tgt] ~ ~ ~ 0.8 1.1
