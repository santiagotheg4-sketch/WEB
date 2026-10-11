execute if score @s dv.timer matches 1.. run tellraw @a[tag=dv_talker] {"text":"La nevera está vacía. Huele raro.","color":"gray","italic":true}
execute unless score @s dv.timer matches 1.. run function canon:furn/fridge_open
playsound minecraft:block.iron_door.open block @a[distance=..12] ~ ~ ~ 0.5 1.6
