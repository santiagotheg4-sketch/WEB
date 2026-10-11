scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=zombie,tag=dv_mariana,distance=..8] if score @s dv.id = #id dv.tmp at @s run function canon:mariana/start_kill
