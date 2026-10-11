summon minecraft:item_display ~ ~0.6 ~ {Tags:["dv_nota_vis","dv_bnew"],brightness:{sky:15,block:15},billboard:"vertical",view_range:0.5f,item:{id:"minecraft:paper",Count:1b},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:interaction ~ ~0.1 ~ {Tags:["dv_nota","dv_click","dv_npc_click","dv_bnew"],width:1.0f,height:1.2f,response:1b}
scoreboard players operation @e[tag=dv_bnew] dv.id = #next dv.id
scoreboard players add #next dv.id 1
tag @e[tag=dv_bnew] remove dv_bnew
