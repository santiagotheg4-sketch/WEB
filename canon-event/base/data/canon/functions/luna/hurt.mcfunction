scoreboard players set @s dv.mode 6
scoreboard players set @s dv.timer 0
execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~180 0
playsound minecraft:entity.wolf.hurt neutral @a[distance=..16] ~ ~ ~ 1 1.6
playsound minecraft:entity.wolf.whine neutral @a[distance=..16] ~ ~ ~ 0.8 1.5
function canon:luna/say_sad
scoreboard players remove #llove dv.dev 5
