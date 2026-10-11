execute positioned ~2 ~ ~2 run function canon:miron/spawn_here
execute as @e[type=zombie,tag=dv_miron,distance=..8] run scoreboard players set @s dv.timer2 1
playsound canon:miron.aparece hostile @a[tag=dv_kpart] ~ ~ ~ 1 0.9
