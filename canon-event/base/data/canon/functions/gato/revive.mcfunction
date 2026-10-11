function canon:spawn/gato
tag @e[type=cave_spider,tag=dv_gato,distance=..1,limit=1,sort=nearest] add dv_revived
playsound canon:gato.growl hostile @a[distance=..16] ~ ~ ~ 1 0.6
particle minecraft:large_smoke ~ ~0.3 ~ 0.2 0.1 0.2 0.01 12 normal
kill @s
