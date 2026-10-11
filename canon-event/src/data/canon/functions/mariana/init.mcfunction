function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320017
attribute @s minecraft:generic.follow_range base set 0
attribute @s minecraft:generic.movement_speed base set 0.42
attribute @s minecraft:generic.attack_damage base set 0
attribute @s minecraft:zombie.spawn_reinforcements base set 0
attribute @s minecraft:generic.knockback_resistance base set 1
scoreboard players set @s dv.talk 0
scoreboard players set @s dv.talkdec 0
scoreboard players set @s dv.music 0
summon minecraft:interaction ~ ~ ~ {Tags:["dv_link","dv_click","dv_mari_click","dv_new_link"],width:0.8f,height:1.95f,response:1b}
summon minecraft:text_display ~ ~2.25 ~ {Tags:["dv_link","dv_mari_bubble","dv_new_link"],billboard:"center",text:'{"text":""}',background:0,see_through:0b,shadow:1b,view_range:0.5f}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
