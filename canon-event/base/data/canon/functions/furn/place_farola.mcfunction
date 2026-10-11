execute align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:item_display ~ ~ ~ {Tags:["dv_mueble","dv_mueble_farola","dv_furn_new"],item_display:"none",view_range:1.5f,brightness:{sky:0,block:15},item:{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7320064}},transformation:{translation:[0f,0.75f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
execute align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:interaction ~ ~ ~ {Tags:["dv_click","dv_furn","dv_furn_farola","dv_furn_new"],width:0.6f,height:2.8f,response:1b}
function canon:furn/orient
execute if block ~ ~2 ~ minecraft:air run setblock ~ ~2 ~ minecraft:light[level=15,waterlogged=false]
tag @e[tag=dv_furn_new] remove dv_furn_new
playsound minecraft:block.wood.place block @a[distance=..16] ~ ~ ~ 1 0.8
kill @s
