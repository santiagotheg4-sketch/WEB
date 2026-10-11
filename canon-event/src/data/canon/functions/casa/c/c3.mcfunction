scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Estoy bien. A veces escucho a alguien caminando arriba, cuando no hay nadie.", "color": "#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 140
tellraw @a[distance=..10] [{"text": "Juli: ", "color": "#f2a7c3"},{"text": "Estoy bien. A veces escucho a alguien caminando arriba, cuando no hay nadie.", "color": "white", "italic": true}]
tellraw @a[tag=dv_jtalk] ["",{"text": "\n\n", "color": "#f2a7c3"},{"text": " [Vamos a ver] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.jr set 8"}},{"text": " [Mejor no] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.jr set 9"}}]
