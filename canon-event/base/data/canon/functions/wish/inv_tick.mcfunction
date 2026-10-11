scoreboard players remove @s dv.inv 1
execute if score #m20 dv.clock matches 0 run particle minecraft:wax_on ~ ~1 ~ 0.4 0.6 0.4 0 3 normal
execute if score @s dv.inv matches 0 run function canon:wish/inv_end
