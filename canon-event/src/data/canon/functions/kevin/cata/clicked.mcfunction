scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Busquen la llave. Debe estar en el rincón más lejano. Siempre está en el rincón más lejano.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 100
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Busquen la llave. Debe estar en el rincón más lejano. Siempre está en el rincón más lejano.", "color": "white", "italic": true}]
