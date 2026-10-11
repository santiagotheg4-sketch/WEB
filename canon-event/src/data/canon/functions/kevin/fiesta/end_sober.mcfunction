scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Bro... ¿viste eso? ¿Quién era ese man flaco? Mejor no volvamos a esa fiesta. O sí. Jajaja.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 160
tellraw @a[distance=..40] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Bro... ¿viste eso? ¿Quién era ese man flaco? Mejor no volvamos a esa fiesta. O sí. Jajaja.", "color": "white", "italic": true}]
