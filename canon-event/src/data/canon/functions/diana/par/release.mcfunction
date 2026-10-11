scoreboard players set @s dv.par 0
effect clear @s minecraft:slowness
effect clear @s minecraft:jump_boost
effect clear @s minecraft:resistance
effect clear @s minecraft:mining_fatigue
stopsound @s master canon:diana.paralysis
scoreboard players operation #pid dv.tmp = @s dv.pid
execute as @e[type=marker,tag=dv_panchor] if score @s dv.target = #pid dv.tmp run kill @s
title @s times 0 6 30
title @s subtitle ""
title @s title ["",{"text":"","font":"canon:susto","color":"white"}]
