scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_xbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Aquí abajo nadie oye tus gritos.", "color": "#b9b9c6"}',background:1342177280}
scoreboard players set @s dv.say 80
tellraw @a[tag=dv_wtgt] [{"text": "Nicolás: ", "color": "#8a8a96"},{"text": "Aquí abajo nadie oye tus gritos.", "color": "white", "italic": true}]
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320131
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320131
scoreboard players set #k dv.tmp 1
