execute if score #flip dv.cfg matches 0 on passengers if entity @s[tag=dv_head,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0f,1f,0f],translation:[0f,0f,0.5697f]}}
execute if score #flip dv.cfg matches 1 on passengers if entity @s[tag=dv_head,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0f,1f,0f],translation:[0f,0f,-0.5697f]}}
execute on passengers if entity @s[tag=dv_neck,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f]}}
scoreboard players set #hy dv.tmp 768
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run function canon:diana/pose/set_y
scoreboard players set #hy dv.tmp 1424
execute on passengers if entity @s[tag=dv_neck,tag=dv_ready] run function canon:diana/pose/set_y
scoreboard players set @s dv.posecur 1
