execute if score #miron dv.cfg matches 1 in canon:sueno_blanco unless entity @e[type=zombie,tag=dv_miron,x=8,y=72,z=8,distance=..30] positioned 8.5 72 2.5 if entity @a[distance=..12] run function canon:miron/spawn_here
execute in canon:sueno_blanco positioned 8.5 72 2.5 run playsound canon:miron.respira hostile @a[distance=..16] ~ ~ ~ 1 0.8
