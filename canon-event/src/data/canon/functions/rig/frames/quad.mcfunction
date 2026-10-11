scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #8 dv.math
execute if score #moving dv.tmp matches 1 if score #c dv.tmp matches 0..1 run scoreboard players set #frame dv.tmp 1
execute if score #moving dv.tmp matches 1 if score #c dv.tmp matches 4..5 run scoreboard players set #frame dv.tmp 2
