execute unless predicate canon:en_sueno run function canon:travel/store_return
scoreboard players set @s dv.sueno 12000
scoreboard players set @s dv.sfase 1
execute in canon:el_sueno run tp @s 0.5 200 4.5 180 10
effect give @s minecraft:slow_falling 8 0 true
effect give @s minecraft:resistance 8 4 true
title @s times 0 40 30
title @s subtitle ""
title @s title ["",{"text":"","font":"canon:susto","color":"white"}]
execute if score #sueno_built dv.build matches 0 run function canon:sueno/build_start
