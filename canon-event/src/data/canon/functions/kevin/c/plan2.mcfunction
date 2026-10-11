scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Quiero grabar un video en el bosque. Dicen que ahí vive un man altísimo, sin cara. Ideal para mi canal.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 160
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Quiero grabar un video en el bosque. Dicen que ahí vive un man altísimo, sin cara. Ideal para mi canal.", "color": "white", "italic": true}]
tellraw @a[tag=dv_ktalk] ["",{"text": "\nEL BOSQUE (de noche, en un bosque)\n", "color": "#ffb347"},{"text": " [Vamos] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.kv set 12"}},{"text": " [Ni loco] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.kv set 5"}}]
