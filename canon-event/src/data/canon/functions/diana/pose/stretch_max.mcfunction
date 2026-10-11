execute if score #flip dv.cfg matches 0 on passengers if entity @s[tag=dv_head,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:18,transformation:{left_rotation:[0f,0f,0.19081f,0.98163f],translation:[0f,0f,0.55f]}}
execute if score #flip dv.cfg matches 0 on passengers if entity @s[tag=dv_neck,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:18,transformation:{scale:[1f,1.229f,1f],left_rotation:[0.22988f,0f,0f,0.97322f],translation:[0f,0f,0f]}}
execute if score #flip dv.cfg matches 1 on passengers if entity @s[tag=dv_head,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:18,transformation:{left_rotation:[0f,0f,0.19081f,0.98163f],translation:[0f,0f,-0.55f]}}
execute if score #flip dv.cfg matches 1 on passengers if entity @s[tag=dv_neck,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:18,transformation:{scale:[1f,1.229f,1f],left_rotation:[-0.22988f,0f,0f,0.97322f],translation:[0f,0f,0f]}}
scoreboard players set #hy dv.tmp 2524
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run function canon:diana/pose/set_y
scoreboard players set #hy dv.tmp 1424
execute on passengers if entity @s[tag=dv_neck,tag=dv_ready] run function canon:diana/pose/set_y
scoreboard players set @s dv.posecur 5
