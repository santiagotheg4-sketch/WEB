scoreboard players set @s dv.state 0
function canon:diana/expr/crawl_scream
playsound canon:diana.scream hostile @a[distance=..48] ~ ~ ~ 1.6 1.5
playsound canon:diana.crack hostile @a[distance=..16] ~ ~ ~ 1 1.3
particle minecraft:dust 0.55 0.05 0.05 1.6 ~ ~0.6 ~ 0.4 0.4 0.4 0 30 normal
execute as @a[tag=dv_dtgt] run function canon:diana/hunt_survived
function canon:diana/vanish
