scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Encontré una entrada a unas catacumbas. Huele a muerto. ¿Bajamos?", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 140
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Encontré una entrada a unas catacumbas. Huele a muerto. ¿Bajamos?", "color": "white", "italic": true}]
tellraw @a[tag=dv_ktalk] ["",{"text": "\nLAS CATACUMBAS\n", "color": "#ffb347"},{"text": " [Bajemos] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.kv set 13"}},{"text": " [Otro día] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.kv set 5"}}]
