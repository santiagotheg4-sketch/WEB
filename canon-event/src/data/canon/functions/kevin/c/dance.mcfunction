scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡Mírame! Paso prohibido número 7.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 100
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¡Mírame! Paso prohibido número 7.", "color": "white", "italic": true}]
tag @s add dv_kdance
scoreboard players set @s dv.timer2 120
function canon:kevin/laugh
scoreboard players set @s dv.timer2 120
