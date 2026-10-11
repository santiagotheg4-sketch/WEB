scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¿Dónde dejé mi collar? Ah, lo tengo puesto. Jaja.", "color": "#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 110
tellraw @a[distance=..10] [{"text": "Juli: ", "color": "#f2a7c3"},{"text": "¿Dónde dejé mi collar? Ah, lo tengo puesto. Jaja.", "color": "white", "italic": true}]
scoreboard players set #k dv.tmp 1
