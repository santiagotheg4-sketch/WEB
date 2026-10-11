execute unless entity @s[tag=dv_moving] run function canon:car/go
data modify storage canon:tmp r set from entity @s Rotation[0]
execute on passengers if entity @s[type=item_display] run data modify entity @s Rotation[0] set from storage canon:tmp r
execute if score @s dv.car matches 2.. if score #m40 dv.clock matches 0 run playsound canon:car.idle neutral @a[distance=..28] ~ ~ ~ 0.9 1
