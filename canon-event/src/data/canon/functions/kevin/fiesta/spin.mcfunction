scoreboard players operation #c dv.tmp = #kt dv.dev
scoreboard players operation #c dv.tmp %= #40 dv.math
execute if score #c dv.tmp matches 0..19 as @e[type=block_display,tag=dv_flight] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{left_rotation:[0f,0.7071f,0f,0.7071f],scale:[1.3f,1.3f,1.3f]}}
execute if score #c dv.tmp matches 20..39 as @e[type=block_display,tag=dv_flight] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
