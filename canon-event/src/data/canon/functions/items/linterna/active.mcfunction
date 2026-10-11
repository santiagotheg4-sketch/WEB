scoreboard players remove @s dv.bat 1
execute if score #m20 dv.clock matches 0 unless score @s dv.bat matches ..600 run effect give @s minecraft:night_vision 12 0 true
execute if score #m20 dv.clock matches 0 if score @s dv.bat matches ..600 if predicate canon:azar/50 run effect give @s minecraft:night_vision 12 0 true
execute if score #m20 dv.clock matches 0 if score @s dv.bat matches ..600 if predicate canon:azar/50 run effect clear @s minecraft:night_vision
execute if score #m4 dv.clock matches 1 anchored eyes positioned ^ ^ ^1.5 run particle minecraft:dust 1 0.95 0.7 0.7 ^ ^ ^ 0.05 0.05 0.05 0 2 normal
execute if score #m4 dv.clock matches 1 anchored eyes positioned ^ ^ ^3.5 run particle minecraft:dust 1 0.95 0.7 0.9 ^ ^ ^ 0.15 0.15 0.15 0 2 normal
execute if score #m4 dv.clock matches 1 anchored eyes positioned ^ ^ ^6 run particle minecraft:dust 1 0.95 0.7 1.1 ^ ^ ^ 0.3 0.3 0.3 0 2 normal
execute if score #m2 dv.clock matches 0 if entity @e[type=zombie,tag=dv_diana,distance=..26] run function canon:items/linterna/ray_start
execute if score @s dv.bat matches ..0 run function canon:items/linterna/dead
