function canon:rig/init_common
scoreboard players operation @s dv.target = #lgen dv.dev
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320104
scoreboard players set @s dv.say -1
scoreboard players set @s dv.idle 0
scoreboard players set @s dv.talkcd 0
scoreboard players set @s dv.jeal 0
summon minecraft:interaction ~ ~ ~ {Tags:["dv_link","dv_click","dv_luna_click","dv_new_link"],width:0.95f,height:0.95f,response:1b}
summon minecraft:text_display ~ ~1.25 ~ {Tags:["dv_link","dv_luna_bubble","dv_new_link"],billboard:"center",text:'{"text":""}',background:0,see_through:0b,shadow:1b,view_range:0.45f,line_width:150,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
