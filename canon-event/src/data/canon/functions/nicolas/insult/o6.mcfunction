scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_xbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Eres lento. Eres débil. Eres mío.", "color": "#b9b9c6"}',background:1342177280}
scoreboard players set @s dv.say 80
tellraw @a[tag=dv_wtgt] [{"text": "Nicolás: ", "color": "#8a8a96"},{"text": "Eres lento. Eres débil. Eres mío.", "color": "white", "italic": true}]
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320130
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320130
scoreboard players set #k dv.tmp 1
