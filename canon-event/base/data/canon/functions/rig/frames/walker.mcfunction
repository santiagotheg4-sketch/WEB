scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if score #moving dv.tmp matches 1 if score #c dv.tmp matches 0..2 run scoreboard players set #frame dv.tmp 1
execute if score #moving dv.tmp matches 1 if score #c dv.tmp matches 6..8 run scoreboard players set #frame dv.tmp 2
