damage @a[distance=..2.6,gamemode=!spectator,gamemode=!creative,limit=1,sort=nearest] 5 canon:abrazo by @s
effect give @a[distance=..2.6] minecraft:slowness 2 2 true
execute as @a[distance=..2.6] run function canon:fx/shake_small
playsound canon:devota.giggle hostile @a[distance=..16] ~ ~ ~ 0.9 1.5
scoreboard players set @s dv.jeal 32
