data merge entity @s {EggLayTime:999999999}
scoreboard players remove @s[scores={dv.timer2=1..}] dv.timer2 1
execute if score @s dv.timer2 matches ..0 if entity @a[distance=..5,predicate=!canon:agachado] run function canon:cuervo/flee
execute if predicate canon:azar/1en600 run playsound canon:animals.crow ambient @a[distance=..32] ~ ~ ~ 0.7 1
