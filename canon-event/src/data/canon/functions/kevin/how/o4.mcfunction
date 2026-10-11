scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Mejor que nunca. Bueno, mejor que la semana pasada, que me perdí tres días.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 120
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Mejor que nunca. Bueno, mejor que la semana pasada, que me perdí tres días.", "color": "white", "italic": true}]
scoreboard players set #k dv.tmp 1
