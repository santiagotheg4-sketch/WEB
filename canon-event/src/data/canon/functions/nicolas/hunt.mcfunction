execute if entity @a[tag=dv_wtgt,distance=1.5..] run function canon:nicolas/step
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #90 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:nicolas.pasos hostile @a[distance=..24] ~ ~ ~ 1 0.9
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #140 dv.math
execute if score #c dv.tmp matches 20 run function canon:nicolas/insult
scoreboard players remove @s[scores={dv.timer2=1..}] dv.timer2 1
execute if entity @a[tag=dv_wtgt,distance=..3] run tag @s add dv_nreach
execute if entity @a[tag=dv_wtgt,distance=..1.6] unless score @s dv.timer2 matches 1.. run function canon:nicolas/hit
