scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Toma, prueba esto. Te va a encantar. Confía en mí.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 120
tellraw @a[tag=dv_kpart] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Toma, prueba esto. Te va a encantar. Confía en mí.", "color": "white", "italic": true}]
tag @s add dv_koffer
tellraw @a[tag=dv_kpart] ["",{"text": "\nKevin te ofrece un vaso con algo brillante...\n", "color": "#ff5ad1"},{"text": " [Tomar] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.kv set 21"}},{"text": " [No, gracias] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.kv set 22"}}]
