playsound canon:gato.hiss hostile @a[distance=..16] ~ ~ ~ 0.8 0.75
execute if predicate canon:azar/50 run playsound canon:gato.growl hostile @a[distance=..16] ~ ~ ~ 0.6 1
scoreboard players set @s dv.timer2 100
execute if predicate canon:azar/50 run scoreboard players add @s dv.timer2 100
