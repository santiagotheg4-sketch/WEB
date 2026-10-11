scoreboard players set #yaw dv.tmp 0
execute store result score #yaw dv.tmp run data get entity @p[distance=..10] Rotation[0]
scoreboard players add #yaw dv.tmp 36045
scoreboard players operation #yaw dv.tmp %= #360 dv.math
scoreboard players operation #yaw dv.tmp /= #90 dv.math
scoreboard players add #yaw dv.tmp 2
scoreboard players operation #yaw dv.tmp %= #4 dv.math
scoreboard players operation #yaw4 dv.tmp = #yaw dv.tmp
