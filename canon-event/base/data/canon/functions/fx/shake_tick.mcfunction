scoreboard players remove @s dv.shake 1
execute if data entity @s RootVehicle run scoreboard players set @s dv.shake 0
scoreboard players operation #sp dv.tmp = @s dv.shake
scoreboard players operation #sp dv.tmp %= #2 dv.math
execute if score @s dv.shake matches 9.. if score #sp dv.tmp matches 0 run tp @s ~ ~ ~ ~3.2 ~-2.4
execute if score @s dv.shake matches 9.. if score #sp dv.tmp matches 1 run tp @s ~ ~ ~ ~-3.2 ~2.4
execute if score @s dv.shake matches 1..8 if score #sp dv.tmp matches 0 run tp @s ~ ~ ~ ~1.4 ~-1.0
execute if score @s dv.shake matches 1..8 if score #sp dv.tmp matches 1 run tp @s ~ ~ ~ ~-1.4 ~1.0
