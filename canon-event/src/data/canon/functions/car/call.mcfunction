scoreboard players set @s dv.cool 40
scoreboard players operation #pid dv.tmp = @s dv.pid
execute as @e[type=horse,tag=dv_car] if score @s dv.car matches 3 if score @s dv.target = #pid dv.tmp at @s run function canon:car/remove
execute rotated ~ 0 positioned ^ ^ ^3 run function canon:car/spawn_player
playsound canon:car.horn neutral @a[distance=..24] ~ ~ ~ 0.8 1.1
