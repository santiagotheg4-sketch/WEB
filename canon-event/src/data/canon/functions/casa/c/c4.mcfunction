scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Está bien. Cierra los ojos y cuenta hasta tres. Vuelve cuando quieras.", "color": "#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 80
tellraw @a[distance=..10] [{"text": "Juli: ", "color": "#f2a7c3"},{"text": "Está bien. Cierra los ojos y cuenta hasta tres. Vuelve cuando quieras.", "color": "white", "italic": true}]
execute as @a[tag=dv_jtalk] at @s run function canon:casa/wake
