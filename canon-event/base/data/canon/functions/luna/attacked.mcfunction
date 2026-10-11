scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=wolf,tag=dv_luna,distance=..8] if score @s dv.id = #id dv.tmp at @s run function canon:luna/hurt
