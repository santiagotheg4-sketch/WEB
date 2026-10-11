scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "La fiesta es de noche, parce. Vuelve a hablarme cuando oscurezca.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 100
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "La fiesta es de noche, parce. Vuelve a hablarme cuando oscurezca.", "color": "white", "italic": true}]
