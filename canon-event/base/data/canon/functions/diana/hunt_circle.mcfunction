execute facing entity @a[tag=dv_dtgt,limit=1] feet rotated ~85 0 positioned ^ ^ ^0.18 rotated ~-85 0 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
execute if score #m20 dv.clock matches 0 if predicate canon:azar/1en4 run playsound canon:diana.scream hostile @a[distance=..32] ~ ~ ~ 1 1.4
execute if score #m10 dv.clock matches 0 run particle minecraft:smoke ~ ~0.5 ~ 0.3 0.2 0.3 0.01 6 normal
