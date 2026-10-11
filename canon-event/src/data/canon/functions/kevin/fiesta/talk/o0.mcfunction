scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡Súbele, súbele! Ah no, no hay volumen. Es mi cabeza.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 80
tellraw @a[tag=dv_kpart] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¡Súbele, súbele! Ah no, no hay volumen. Es mi cabeza.", "color": "white", "italic": true}]
scoreboard players set #k dv.tmp 1
