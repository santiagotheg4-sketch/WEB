execute store result score @s dv.rx run data get entity @s Pos[0]
execute store result score @s dv.ry run data get entity @s Pos[1]
execute store result score @s dv.rz run data get entity @s Pos[2]
scoreboard players set @s dv.rdim 0
execute if predicate canon:en_nether run scoreboard players set @s dv.rdim 1
execute if predicate canon:en_end run scoreboard players set @s dv.rdim 2
