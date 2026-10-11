scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¿Sabes cuál es el colmo de un fantasma? Que lo dejen en visto.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 140
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¿Sabes cuál es el colmo de un fantasma? Que lo dejen en visto.", "color": "white", "italic": true}]
function canon:kevin/laugh
scoreboard players set #k dv.tmp 1
