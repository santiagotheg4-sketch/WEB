particle minecraft:soul_fire_flame ~ ~0.3 ~ 0.2 0.3 0.2 0.02 20 normal
particle minecraft:large_smoke ~ ~0.5 ~ 0.2 0.4 0.2 0.01 15 normal
playsound minecraft:block.fire.extinguish block @a[distance=..16] ~ ~ ~ 1 0.6
playsound canon:diana.hum hostile @a[distance=..16] ~ ~ ~ 0.6 1.2
execute as @a[distance=..10] run function canon:diana/ofrenda_player
kill @s
