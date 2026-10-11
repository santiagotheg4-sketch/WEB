scoreboard players set #kt dv.dev 0
execute as @a[tag=dv_kpart] at @s run function canon:travel/store_return
execute as @a[tag=dv_kpart] in minecraft:overworld run tp @s 20003.5 -49 20003.5 -90 0
execute as @a[tag=dv_kpart] run effect give @s minecraft:darkness 3 0 true
execute as @e[type=zombie,tag=dv_kevin] in minecraft:overworld run tp @s 20003.5 -49 20002.5
playsound canon:cata.reja master @a[tag=dv_kpart] ~ ~ ~ 1 0.8
playsound canon:cata.ambient ambient @a[tag=dv_kpart] ~ ~ ~ 1 1
title @a[tag=dv_kpart] times 10 60 20
title @a[tag=dv_kpart] subtitle {"text":"Encuentra la llave de la reja. Algo se arrastra ahí abajo.","color":"gray","italic":true}
title @a[tag=dv_kpart] title {"text":"LAS CATACUMBAS","color":"#9a9a9a"}
kill @e[type=interaction,tag=dv_cllave]
kill @e[type=item_display,tag=dv_cllave_vis]
kill @e[type=interaction,tag=dv_creja]
execute in minecraft:overworld run summon minecraft:item_display 20033.5 -49.4 20038.5 {Tags:["dv_cllave_vis"],brightness:{sky:12,block:12},billboard:"vertical",item:{id:"minecraft:tripwire_hook",Count:1b},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f],right_rotation:[0f,0f,0f,1f]}}
execute in minecraft:overworld run summon minecraft:interaction 20033.5 -49 20038.5 {Tags:["dv_cllave","dv_click","dv_npc_click"],width:1.0f,height:1.0f,response:1b}
execute in minecraft:overworld run summon minecraft:interaction 20040.5 -49 20038.5 {Tags:["dv_creja","dv_click","dv_npc_click"],width:1.2f,height:3.0f,response:1b}
execute in minecraft:overworld run fill 20040 -49 20037 20040 -47 20039 minecraft:iron_bars
