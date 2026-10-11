execute if score #flip dv.cfg matches 0 on passengers if entity @s[tag=dv_head,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:40,transformation:{left_rotation:[0f,0f,-0.10453f,0.99452f],translation:[0f,0f,0.3f]}}
execute if score #flip dv.cfg matches 0 on passengers if entity @s[tag=dv_neck,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:40,transformation:{scale:[1f,0.761f,1f],left_rotation:[0.20125f,0f,0f,0.97954f],translation:[0f,0f,0f]}}
execute if score #flip dv.cfg matches 1 on passengers if entity @s[tag=dv_head,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:40,transformation:{left_rotation:[0f,0f,-0.10453f,0.99452f],translation:[0f,0f,-0.3f]}}
execute if score #flip dv.cfg matches 1 on passengers if entity @s[tag=dv_neck,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:40,transformation:{scale:[1f,0.761f,1f],left_rotation:[-0.20125f,0f,0f,0.97954f],translation:[0f,0f,0f]}}
scoreboard players set #hy dv.tmp 2124
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run function canon:diana/pose/set_y
scoreboard players set #hy dv.tmp 1424
execute on passengers if entity @s[tag=dv_neck,tag=dv_ready] run function canon:diana/pose/set_y
scoreboard players set @s dv.posecur 4
