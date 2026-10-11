scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #4 dv.math
execute if score #moving dv.tmp matches 1 if score #c dv.tmp matches 0..1 run scoreboard players set #frame dv.tmp 1
execute if data storage canon:tmp e{OnGround:0b} if score #c dv.tmp matches 0..1 run scoreboard players set #frame dv.tmp 2
execute if data storage canon:tmp e{OnGround:0b} if score #c dv.tmp matches 2..3 run scoreboard players set #frame dv.tmp 3
