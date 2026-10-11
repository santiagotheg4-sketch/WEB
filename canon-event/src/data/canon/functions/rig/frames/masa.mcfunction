scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #24 dv.math
execute if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 1
execute if score #c dv.tmp matches 18..23 run scoreboard players set #frame dv.tmp 2
