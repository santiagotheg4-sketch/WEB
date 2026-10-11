execute if score @s dv.timer matches 1..30 rotated ~ 0 positioned ^ ^ ^0.25 run tp @s ~ ~ ~ ~ ~
execute if score @s dv.timer matches 1..30 run tag @s add dv_lrun
execute if score @s dv.timer matches 1..30 at @s run function canon:diana/ground
execute if score @s dv.timer matches 90.. run scoreboard players set @s dv.mode 0
