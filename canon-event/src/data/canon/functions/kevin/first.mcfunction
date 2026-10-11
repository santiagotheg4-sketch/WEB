scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡Eyyy! Soy Kevin. Tú no me conoces, pero yo a ti sí. Tengo planes. Muchos planes.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 140
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¡Eyyy! Soy Kevin. Tú no me conoces, pero yo a ti sí. Tengo planes. Muchos planes.", "color": "white", "italic": true}]
tellraw @a[distance=..20] {"text": "(Haz clic derecho en Kevin para hablar con él. Te contará chistes y te llevará a sus aventuras.)", "color": "gray", "italic": true}
scoreboard players set #kprog dv.dev 1
