execute if score #m40 dv.clock matches 0 run particle minecraft:note ~ ~0.7 ~ 0.1 0.1 0.1 0 1 normal
execute if score @s dv.timer matches 600 run function canon:luna/sleep_talk
execute if entity @a[tag=dv_ltgt,distance=6..] run function canon:luna/wake
execute if entity @a[tag=dv_ltgt,distance=..6,scores={dv.noise=3..}] run function canon:luna/wake
