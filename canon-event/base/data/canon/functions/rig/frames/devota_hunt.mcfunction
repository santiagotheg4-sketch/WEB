scoreboard players set #frame dv.tmp 3
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #10 dv.math
execute if score #moving dv.tmp matches 1 if score #c dv.tmp matches 5..9 run scoreboard players set #frame dv.tmp 4
