particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 25 normal
particle minecraft:dust 0.85 0.4 0.5 1.4 ~ ~1 ~ 0.3 0.6 0.3 0 20 normal
playsound canon:devota.whisper hostile @a[distance=..16] ~ ~ ~ 0.8 0.8
damage @s 40 minecraft:magic
execute as @e[type=zombie,tag=dv_devota,distance=..30,limit=1,sort=nearest] at @s run function canon:devota/protect_say
