tag @s add dv_moving
playsound minecraft:block.iron_door.open neutral @a[distance=..16] ~ ~ ~ 0.6 1.3
execute if score @s dv.car matches 2.. run attribute @s minecraft:generic.movement_speed base set 0.34
execute if score @s dv.car matches 2.. run playsound canon:car.start neutral @a[distance=..32] ~ ~ ~ 1 1
execute as @e[type=item_display,tag=dv_carbody,distance=..6] if score @s dv.id = #id dv.tmp run function canon:car/body_ride
