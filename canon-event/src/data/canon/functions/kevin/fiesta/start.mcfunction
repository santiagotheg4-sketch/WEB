scoreboard players set #kev dv.dev 1
scoreboard players set #kt dv.dev 0
scoreboard players set #kdrunk dv.dev 0
tag @a[gamemode=!spectator,distance=..32] add dv_kpart
kill @e[type=marker,tag=dv_fiesta_c]
summon minecraft:marker ~ ~ ~ {Tags:["dv_fiesta_c"]}
scoreboard players set @s dv.mode 1
tag @s add dv_kdance
execute positioned ~3 ~ ~ run function canon:kevin/fiesta/dancer_0
execute positioned ~-3 ~ ~1 run function canon:kevin/fiesta/dancer_1
execute positioned ~1 ~ ~3 run function canon:kevin/fiesta/dancer_2
execute positioned ~-1 ~ ~-3 run function canon:kevin/fiesta/dancer_0
execute positioned ~3 ~ ~-3 run function canon:kevin/fiesta/dancer_1
execute positioned ~-3 ~ ~3 run function canon:kevin/fiesta/dancer_2
execute positioned ~ ~6 ~ run summon minecraft:block_display ~-2 ~ ~ {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:magenta_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~6 ~ run summon minecraft:block_display ~2 ~ ~ {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:cyan_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~6 ~ run summon minecraft:block_display ~ ~ ~2 {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:lime_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~6 ~ run summon minecraft:block_display ~ ~ ~-2 {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:yellow_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
playsound canon:kevin.techno record @a[tag=dv_kpart] ~ ~ ~ 1 1
title @a[tag=dv_kpart] times 10 50 20
title @a[tag=dv_kpart] subtitle {"text":"La mejor fiesta del mundo. La única.","color":"#ffd27a","italic":true}
title @a[tag=dv_kpart] title {"text":"FIESTA TECHNO","color":"#ff5ad1","bold":true}
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡EYYY! ¡Bienvenidos a la mejor fiesta del mundo! ¡A bailar!", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 120
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¡EYYY! ¡Bienvenidos a la mejor fiesta del mundo! ¡A bailar!", "color": "white", "italic": true}]
