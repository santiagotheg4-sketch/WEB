execute if entity @s[tag=dv_shook] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0f,0f,1f]}}
execute unless entity @s[tag=dv_shook] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0f,0.0262f,0.9997f]}}
execute if entity @s[tag=dv_shook] run tag @s add dv_unshook
tag @s[tag=!dv_unshook] add dv_shook
tag @s[tag=dv_unshook] remove dv_shook
tag @s remove dv_unshook
