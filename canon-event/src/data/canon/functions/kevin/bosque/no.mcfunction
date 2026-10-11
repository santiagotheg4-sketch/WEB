scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Tiene que ser de noche y en un bosque de verdad, con árboles. Llévame a uno y me hablas.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 120
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Tiene que ser de noche y en un bosque de verdad, con árboles. Llévame a uno y me hablas.", "color": "white", "italic": true}]
