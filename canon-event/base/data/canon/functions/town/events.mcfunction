scoreboard players remove #apagon_cd dv.ev 1
execute if score #apagon dv.ev matches 1.. run scoreboard players remove #apagon dv.ev 1
execute if score #apagon dv.ev matches 1 run function canon:town/apagon_end
execute if score #apagon dv.ev matches ..0 if score #apagon_cd dv.ev matches ..0 if score #clima dv.cfg matches 1 if predicate canon:azar/1en20 run function canon:town/apagon_start
execute if predicate canon:azar/1en200 run function canon:town/grito
execute if score #clima dv.cfg matches 1 if predicate canon:azar/1en1200 in minecraft:overworld run weather rain 2400
execute if predicate canon:azar/1en100 as @a[predicate=canon:en_pueblo] at @s run playsound canon:ambient.additions ambient @s ~ ~ ~ 0.6 1 0.2
function canon:escape/slow
