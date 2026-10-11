tp @s ~ ~ ~
execute store result score #my dv.tmp run data get entity @s Pos[1] 1000
scoreboard players operation #my dv.tmp += #ly dv.tmp
execute store result entity @s Pos[1] double 0.001 run scoreboard players get #my dv.tmp
