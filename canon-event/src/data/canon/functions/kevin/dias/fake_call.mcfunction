scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_xbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡Eyy! ¡Por aquí! ¡Ven!", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 50
