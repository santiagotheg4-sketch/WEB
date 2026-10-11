tag @s remove dv_moving
attribute @s minecraft:generic.movement_speed base set 0
execute on passengers if entity @s[type=item_display] run function canon:car/body_park
playsound minecraft:block.iron_door.close neutral @a[distance=..16] ~ ~ ~ 0.6 1.3
