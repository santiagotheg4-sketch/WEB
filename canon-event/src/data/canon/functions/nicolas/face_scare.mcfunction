scoreboard players set @s dv.ncd 900
execute anchored eyes positioned ^ ^ ^2.4 run summon minecraft:item_display ~ ~ ~ {Tags:["dv_nface","dv_nface_new"],item_display:"none",brightness:{sky:15,block:12},view_range:0.6f,item:{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7320132}},transformation:{translation:[0f,-0.12f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f],right_rotation:[0f,0f,0f,1f]}}
tag @s add dv_nface_me
execute as @e[type=item_display,tag=dv_nface_new] at @s facing entity @a[tag=dv_nface_me,limit=1] eyes run tp @s ~ ~ ~ ~ 0
tag @s remove dv_nface_me
execute if score #flip dv.cfg matches 1 as @e[type=item_display,tag=dv_nface_new] run data modify entity @s transformation.right_rotation set value [0f,1f,0f,0f]
execute as @e[type=item_display,tag=dv_nface_new] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[2.4f,2.4f,2.4f],translation:[0f,-0.5f,0f]}}
tag @e[type=item_display,tag=dv_nface_new] remove dv_nface_new
playsound canon:nicolas.maldito master @s ~ ~ ~ 1 0.95
playsound canon:fx.stinger master @s ~ ~ ~ 0.9 1
effect give @s minecraft:darkness 3 0 true
title @s times 0 25 10
title @s subtitle {"text":"¡MALDITO!","color":"#b01212","bold":true}
title @s title {"text":" "}
function canon:fx/shake_big
