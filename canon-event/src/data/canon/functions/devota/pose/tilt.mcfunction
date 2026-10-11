execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:24,transformation:{left_rotation:[0f,0f,0.24192f,0.9703f]}}
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{left_rotation:[0f,0f,0f,1f]}}
scoreboard players set #hy dv.tmp 1438
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run function canon:diana/pose/set_y
scoreboard players set #hy dv.tmp 1375
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run function canon:diana/pose/set_y
scoreboard players set @s dv.posecur 2
