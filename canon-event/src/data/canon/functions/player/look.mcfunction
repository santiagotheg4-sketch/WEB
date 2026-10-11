scoreboard players set @s dv.seen 0
scoreboard players set #r dv.tmp 0
tag @s add dv_looker
execute anchored eyes positioned ^ ^ ^0.4 run function canon:player/look_ray
tag @s remove dv_looker
