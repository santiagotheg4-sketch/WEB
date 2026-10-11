scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡Ey, ey, tranquilo! Soy yo, Kevin. El bueno.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 80
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¡Ey, ey, tranquilo! Soy yo, Kevin. El bueno.", "color": "white", "italic": true}]
function canon:kevin/laugh
