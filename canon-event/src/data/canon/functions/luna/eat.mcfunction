scoreboard players set @s dv.mode 5
scoreboard players set @s dv.timer 0
playsound minecraft:entity.generic.eat neutral @a[distance=..12] ~ ~ ~ 0.8 1.4
particle minecraft:heart ~ ~1 ~ 0.3 0.2 0.3 0 4 normal
function canon:luna/say_fed
scoreboard players add #llove dv.dev 3
