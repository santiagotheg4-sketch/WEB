scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡Baila conmigo! Nadie nos está mirando. Creo.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 80
tellraw @a[tag=dv_kpart] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¡Baila conmigo! Nadie nos está mirando. Creo.", "color": "white", "italic": true}]
scoreboard players set #k dv.tmp 1
