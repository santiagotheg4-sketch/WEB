execute as @e[type=zombie,tag=dv_masa] at @s run function canon:rig/despawn
kill @e[type=interaction,tag=dv_cllave]
kill @e[type=item_display,tag=dv_cllave_vis]
kill @e[type=interaction,tag=dv_creja]
tag @a remove dv_kpart
tag @a remove dv_cout
scoreboard players set #kev dv.dev 0
