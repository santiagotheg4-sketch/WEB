scoreboard players remove @s dv.rain 1
execute if score #m4 dv.clock matches 0 positioned ~ ~4 ~ run loot spawn ~ ~ ~ loot canon:deseos/riqueza
execute if score @s dv.rain matches 0 run function canon:wish/riqueza_precio
