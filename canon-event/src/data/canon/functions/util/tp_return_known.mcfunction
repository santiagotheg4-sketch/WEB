execute if score @s dv.rdim matches 0 in minecraft:overworld run tp @s 0 0 0
execute if score @s dv.rdim matches 1 in minecraft:the_nether run tp @s 0 0 0
execute if score @s dv.rdim matches 2 in minecraft:the_end run tp @s 0 0 0
scoreboard players operation #v dv.tmp = @s dv.rx
execute if score #v dv.tmp matches ..-1 run function canon:util/tp_x_neg
execute if score #v dv.tmp matches 0.. run function canon:util/tp_x_pos
scoreboard players operation #v dv.tmp = @s dv.ry
execute if score #v dv.tmp matches ..-1 run function canon:util/tp_y_neg
execute if score #v dv.tmp matches 0.. run function canon:util/tp_y_pos
scoreboard players operation #v dv.tmp = @s dv.rz
execute if score #v dv.tmp matches ..-1 run function canon:util/tp_z_neg
execute if score #v dv.tmp matches 0.. run function canon:util/tp_z_pos
tp @s ~0.5 ~ ~0.5
effect give @s minecraft:slow_falling 4 0 true
effect give @s minecraft:resistance 5 4 true
