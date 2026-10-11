scoreboard players add @s dv.timer 1
execute if score @s dv.timer matches 22 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[0f,0f,0f]}}
execute if score @s dv.timer matches 22 run particle minecraft:large_smoke ~ ~ ~ 0.4 0.4 0.4 0.02 20 normal
execute if score @s dv.timer matches 32.. run kill @s
