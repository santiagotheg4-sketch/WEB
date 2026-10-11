tag @s remove dv_has_bubble
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_mari_bubble,distance=..40] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":""}',background:0}
