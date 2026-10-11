scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "En la casa. La que sueña la gente que duerme cerca de Santi. No sé por qué, pero siempre termino aquí.", "color": "#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 160
tellraw @a[distance=..10] [{"text": "Juli: ", "color": "#f2a7c3"},{"text": "En la casa. La que sueña la gente que duerme cerca de Santi. No sé por qué, pero siempre termino aquí.", "color": "white", "italic": true}]
tellraw @a[tag=dv_jtalk] ["",{"text": "\n\n", "color": "#f2a7c3"},{"text": " [¿Santi?] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.jr set 5"}},{"text": " [¿Por qué todo es blanco?] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.jr set 6"}}]
