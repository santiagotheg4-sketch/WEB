scoreboard players remove @s dv.sueno 1
execute if score @s dv.sueno matches 1200 run title @s actionbar {"text":"El sueño empieza a desvanecerse…","color":"#f2a7c3","italic":true}
execute if score @s dv.sueno matches ..0 run function canon:sueno/wake
execute if entity @s[y=-64,dy=69] run function canon:sueno/wake
execute if score #m40 dv.clock matches 0 run particle minecraft:cherry_leaves ~ ~3 ~ 6 2 6 0 4 normal
