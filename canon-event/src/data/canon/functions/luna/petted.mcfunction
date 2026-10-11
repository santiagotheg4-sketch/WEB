scoreboard players set @s dv.mode 5
scoreboard players set @s dv.timer 0
playsound minecraft:entity.wolf.pant neutral @a[distance=..12] ~ ~ ~ 0.8 1.7
particle minecraft:heart ~ ~1 ~ 0.3 0.2 0.3 0 3 normal
function canon:luna/say_pet
scoreboard players add #llove dv.dev 1
execute as @e[type=zombie,tag=dv_devota,distance=..16] at @s run function canon:luna/devota_sees_pet
