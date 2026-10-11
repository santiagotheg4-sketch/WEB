tag @s remove dv_swayed
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{left_rotation:[0f,0f,0f,1f]}}
