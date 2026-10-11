scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Este DJ es mi primo. Bueno, no tengo primos. Pero ojalá.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 80
tellraw @a[tag=dv_kpart] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Este DJ es mi primo. Bueno, no tengo primos. Pero ojalá.", "color": "white", "italic": true}]
scoreboard players set #k dv.tmp 1
