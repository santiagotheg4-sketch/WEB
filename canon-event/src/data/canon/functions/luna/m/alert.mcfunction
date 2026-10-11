execute if score #m4 dv.clock matches 0 run function canon:luna/face_danger
execute if score @s dv.timer matches 12 run tag @s remove dv_lbark
execute if score @s dv.timer matches 20 run function canon:luna/bark2
execute if score @s dv.timer matches 30 run tag @s remove dv_lbark
execute if score @s dv.timer matches 45.. run scoreboard players set @s dv.mode 4
