scoreboard players set @s dv.timer 3
playsound canon:items.radio_static block @a[distance=..16] ~ ~ ~ 0.5 1
execute if predicate canon:azar/1en3 run playsound canon:items.radio_voice block @a[distance=..16] ~ ~ ~ 0.6 1
execute if predicate canon:azar/1en4 if entity @a[distance=..10,scores={dv.obs=1..}] run playsound canon:devota.whisper block @a[distance=..16] ~ ~ ~ 0.6 1
