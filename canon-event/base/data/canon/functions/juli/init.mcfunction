function canon:rig/init_common
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players operation @s dv.state = #jstate dv.tmp
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320094
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320099
attribute @s minecraft:generic.follow_range base set 0
attribute @s minecraft:generic.knockback_resistance base set 1
scoreboard players set @s dv.say 0
scoreboard players set @s dv.jline 0
summon minecraft:interaction ~ ~ ~ {Tags:["dv_link","dv_click","dv_juli_click","dv_new_link"],width:0.8f,height:1.9f,response:1b}
summon minecraft:text_display ~ ~2.3 ~ {Tags:["dv_link","dv_juli_bubble","dv_new_link"],billboard:"center",text:'{"text":""}',background:0,see_through:0b,shadow:1b,view_range:0.5f,line_width:160}
summon minecraft:marker ~ ~1.55 ~ {Tags:["dv_link","dv_jlook","dv_new_link"]}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
playsound canon:juli.chime ambient @a[distance=..24] ~ ~ ~ 0.8 1
particle minecraft:cherry_leaves ~ ~1 ~ 0.5 1 0.5 0 40 normal
particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.02 12 normal
