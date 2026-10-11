scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Raro. Desde la fiesta escucho música techno en todas partes.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 120
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Raro. Desde la fiesta escucho música techno en todas partes.", "color": "white", "italic": true}]
scoreboard players set #k dv.tmp 1
