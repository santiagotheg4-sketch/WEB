scoreboard players operation #id dv.tmp = @s dv.id
execute if entity @s[tag=dv_kev_click] as @e[type=zombie,tag=dv_kevin,distance=..6] if score @s dv.id = #id dv.tmp at @s run function canon:kevin/attacked
