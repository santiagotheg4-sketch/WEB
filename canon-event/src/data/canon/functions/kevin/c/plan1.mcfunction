scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Esta noche hay una fiesta techno. La mejor del mundo. Bueno, la única. ¿Vienes?", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 140
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Esta noche hay una fiesta techno. La mejor del mundo. Bueno, la única. ¿Vienes?", "color": "white", "italic": true}]
tellraw @a[tag=dv_ktalk] ["",{"text": "\nFIESTA TECHNO (de noche)\n", "color": "#ffb347"},{"text": " [¡Vamos!] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.kv set 11"}},{"text": " [Ahora no] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.kv set 5"}}]
