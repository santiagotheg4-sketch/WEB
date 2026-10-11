scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Espera, que ya estamos en algo.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 60
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Espera, que ya estamos en algo.", "color": "white", "italic": true}]
