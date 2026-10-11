scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Ay. ¿Por qué...? Aquí nadie se hace daño. Solo se olvida.", "color": "#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 90
tellraw @a[distance=..10] [{"text": "Juli: ", "color": "#f2a7c3"},{"text": "Ay. ¿Por qué...? Aquí nadie se hace daño. Solo se olvida.", "color": "white", "italic": true}]
