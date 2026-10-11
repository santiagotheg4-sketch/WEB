scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=interaction,tag=dv_xclick] if score @s dv.id = #id dv.tmp run tp @s ~ ~ ~
execute as @e[type=text_display,tag=dv_xbubble] if score @s dv.id = #id dv.tmp run tp @s ~ ~2.3 ~
