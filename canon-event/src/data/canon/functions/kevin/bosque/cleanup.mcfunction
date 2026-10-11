kill @e[type=item_display,tag=dv_nota_vis]
kill @e[type=interaction,tag=dv_nota]
kill @e[type=marker,tag=dv_bosque_c]
execute as @e[type=zombie,tag=dv_alto] at @s run function canon:rig/despawn
tag @a remove dv_kpart
scoreboard players set #kev dv.dev 0
