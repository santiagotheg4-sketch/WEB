scoreboard players set @s dv.mode 6
scoreboard players set @s dv.timer 0
data merge entity @s {NoAI:1b}
attribute @s minecraft:generic.follow_range base set 0
function canon:devota/expr/cry
playsound canon:devota.whisper hostile @a[distance=..24] ~ ~ ~ 0.8 0.7
