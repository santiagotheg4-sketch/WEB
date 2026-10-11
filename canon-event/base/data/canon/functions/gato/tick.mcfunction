scoreboard players remove @s[scores={dv.timer2=1..}] dv.timer2 1
execute if score @s dv.timer2 matches ..0 if entity @a[distance=..12] run function canon:gato/noise
