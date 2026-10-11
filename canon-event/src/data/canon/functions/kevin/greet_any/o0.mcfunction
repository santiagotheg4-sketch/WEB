scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡Eyyy! ¿Qué más, parce? Te estaba buscando.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 100
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¡Eyyy! ¿Qué más, parce? Te estaba buscando.", "color": "white", "italic": true}]
scoreboard players set #k dv.tmp 1
