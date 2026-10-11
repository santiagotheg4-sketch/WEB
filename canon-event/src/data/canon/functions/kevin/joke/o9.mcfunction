scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Mariana me miró una vez. Una. Ya no tengo cejas.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 140
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Mariana me miró una vez. Una. Ya no tengo cejas.", "color": "white", "italic": true}]
function canon:kevin/laugh
scoreboard players set #k dv.tmp 1
