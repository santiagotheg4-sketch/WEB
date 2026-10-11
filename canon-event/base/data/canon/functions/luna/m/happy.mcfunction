execute if score #m4 dv.clock matches 0 run function canon:luna/face
execute if score #m10 dv.clock matches 0 run particle minecraft:heart ~ ~1 ~ 0.2 0.1 0.2 0 1 normal
execute if score @s dv.timer matches 60.. run scoreboard players set @s dv.mode 0
