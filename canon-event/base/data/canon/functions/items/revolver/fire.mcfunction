clear @s minecraft:iron_nugget{canon:{id:"balas"}} 1
playsound canon:items.revolver_shot player @a[distance=..96] ~ ~ ~ 4 1
scoreboard players set @s dv.noisecd 40
tag @s add dv_shooter
scoreboard players set #ray dv.tmp 0
execute anchored eyes positioned ^ ^ ^0.8 run particle minecraft:smoke ~ ~ ~ 0.05 0.05 0.05 0.02 6 normal
execute anchored eyes positioned ^ ^ ^0.8 run particle minecraft:flash ~ ~ ~ 0 0 0 0 1 normal
execute anchored eyes positioned ^ ^ ^0.6 run function canon:items/revolver/ray
tag @s remove dv_shooter
