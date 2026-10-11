tag @s remove dv_dwasseen
tag @s add dv_dme
scoreboard players set #dr dv.tmp 0
execute as @a[tag=dv_dtgt,limit=1] at @s anchored eyes positioned ^ ^ ^0.6 run function canon:diana/look_ray
tag @s remove dv_dme
execute if score #dr dv.tmp matches 1000 run scoreboard players set #dseen dv.tmp 1
execute if score #dr dv.tmp matches 1000 run tag @s add dv_dwasseen
