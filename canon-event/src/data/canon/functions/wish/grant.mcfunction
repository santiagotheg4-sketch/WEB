clear @s minecraft:carrot_on_a_stick{canon:{id:"hueso_deseo"}} 1
playsound canon:items.wish_crack player @a[distance=..16] ~ ~ ~ 1 1
playsound canon:items.wish_granted player @s ~ ~ ~ 0.9 1
particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.6 0.4 0.03 30 normal
particle minecraft:item minecraft:bone ~ ~1.3 ~ 0.2 0.2 0.2 0.08 12 normal
execute if score @s dv.deseo matches 1 run function canon:wish/amor
execute if score @s dv.deseo matches 2 run function canon:wish/riqueza
execute if score @s dv.deseo matches 3 run function canon:wish/invencible
execute if score @s dv.deseo matches 4 run function canon:wish/desaparecer
execute if score @s dv.deseo matches 5 run function canon:wish/salir
