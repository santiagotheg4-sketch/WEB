function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320115
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320115
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320122
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320122
scoreboard players set @s dv.mode 0
scoreboard players set @s dv.say -1
scoreboard players set @s dv.timer 600
summon minecraft:interaction ~ ~ ~ {Tags:["dv_link","dv_click","dv_npc_click","dv_kev_click","dv_xclick","dv_new_link"],width:0.8f,height:1.95f,response:1b}
function canon:x/add_bubble
