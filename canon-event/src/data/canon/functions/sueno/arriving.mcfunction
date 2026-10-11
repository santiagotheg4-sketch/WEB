scoreboard players add @s dv.sfase 1
execute if score #sueno_built dv.build matches 1 run function canon:sueno/build_try
execute if score #sueno_built dv.build matches 0 run function canon:sueno/build_start
execute if score @s dv.sfase matches 30.. if score #sueno_built dv.build matches 2 run function canon:sueno/arrived
execute if score @s dv.sfase matches 2.. unless score #sueno_built dv.build matches 2 run tp @s 0.5 200 4.5
execute if score @s dv.sfase matches 900.. run function canon:sueno/wake
