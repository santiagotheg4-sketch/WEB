scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¿En serio? Perdí una foto vieja. Búscala en el cuarto de arriba a la izquierda. Ahí siempre se pierden las cosas.", "color": "#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 160
tellraw @a[distance=..10] [{"text": "Juli: ", "color": "#f2a7c3"},{"text": "¿En serio? Perdí una foto vieja. Búscala en el cuarto de arriba a la izquierda. Ahí siempre se pierden las cosas.", "color": "white", "italic": true}]
kill @e[type=interaction,tag=dv_cfoto]
kill @e[type=item_display,tag=dv_cfoto_vis]
execute in canon:sueno_blanco run summon minecraft:item_display 14.5 72.3 12.5 {Tags:["dv_cfoto_vis"],brightness:{sky:15,block:15},billboard:"vertical",item:{id:"minecraft:paper",Count:1b},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.5f,0.5f,0.5f],right_rotation:[0f,0f,0f,1f]}}
execute in canon:sueno_blanco run summon minecraft:interaction 14.5 72 12.5 {Tags:["dv_cfoto","dv_click","dv_npc_click"],width:0.8f,height:0.8f,response:1b}
