scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=zombie,tag=dv_juli,distance=..6] if score @s dv.id = #id dv.tmp at @s run function canon:juli/clicked_me
