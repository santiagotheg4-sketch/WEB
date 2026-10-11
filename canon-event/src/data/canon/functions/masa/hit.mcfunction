scoreboard players set @s dv.timer2 25
damage @a[tag=dv_wtgt,limit=1] 6 minecraft:mob_attack by @s
effect give @a[tag=dv_wtgt] minecraft:slowness 3 2 true
playsound canon:masa.rugido hostile @a[distance=..16] ~ ~ ~ 1 1.3
