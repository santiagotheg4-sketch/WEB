scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡Yo grabo desde allá! ¡Busquen las 6 notas del Alto antes de que los encuentre! Jajaja...", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 120
tellraw @a[tag=dv_kpart] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¡Yo grabo desde allá! ¡Busquen las 6 notas del Alto antes de que los encuentre! Jajaja...", "color": "white", "italic": true}]
particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.02 12 normal
function canon:rig/despawn
