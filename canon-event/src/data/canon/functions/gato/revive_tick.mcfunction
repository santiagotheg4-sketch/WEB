scoreboard players remove @s dv.timer 1
execute if score @s dv.timer matches 1 run particle minecraft:soul ~ ~0.3 ~ 0.3 0.1 0.3 0.01 10 normal
execute if score @s dv.timer matches ..0 run function canon:gato/revive
