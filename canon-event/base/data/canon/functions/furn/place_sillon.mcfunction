execute align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:item_display ~ ~ ~ {Tags:["dv_mueble","dv_mueble_sillon","dv_furn_new"],item_display:"none",view_range:1.5f,item:{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7320063}},transformation:{translation:[0f,0.5f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f],right_rotation:[0f,0f,0f,1f]}}
execute align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:interaction ~ ~ ~ {Tags:["dv_click","dv_furn","dv_furn_sillon","dv_furn_new"],width:1.05f,height:1.2f,response:1b}
function canon:furn/orient
execute if block ~ ~ ~ minecraft:air run setblock ~ ~ ~ minecraft:barrier
tag @e[tag=dv_furn_new] remove dv_furn_new
playsound minecraft:block.wood.place block @a[distance=..16] ~ ~ ~ 1 0.8
kill @s
