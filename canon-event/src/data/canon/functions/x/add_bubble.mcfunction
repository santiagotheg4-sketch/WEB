summon minecraft:text_display ~ ~2.3 ~ {Tags:["dv_link","dv_xbubble","dv_new_link"],billboard:"center",text:'{"text":""}',background:0,see_through:0b,shadow:1b,view_range:0.5f,line_width:170}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
