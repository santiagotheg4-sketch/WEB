stopsound @a[tag=dv_kpart] record canon:kevin.techno
stopsound @a[tag=dv_kdrug] music canon:kevin.drugged
execute as @e[type=zombie,tag=dv_fiestero] at @s run function canon:rig/despawn
kill @e[type=block_display,tag=dv_flight]
kill @e[type=marker,tag=dv_fiesta_c]
execute as @e[type=zombie,tag=dv_miron] at @s run function canon:rig/despawn
execute as @e[type=zombie,tag=dv_kevin] run scoreboard players set @s dv.mode 0
execute as @e[type=zombie,tag=dv_kevin] run tag @s remove dv_kdance
tag @a remove dv_kdrug
tag @a remove dv_kpart
scoreboard players set #kev dv.dev 0
