tag @a remove dv_jtgt
tag @a[predicate=canon:en_casa_sueno,distance=..8,limit=1,sort=nearest] add dv_jtgt
execute unless entity @a[predicate=canon:en_casa_sueno] run function canon:rig/despawn
execute if entity @a[tag=dv_jtgt] if score #m4 dv.clock matches 0 run function canon:juli/face
execute if entity @a[tag=dv_jtgt,distance=2.5..] if entity @a[tag=dv_jtgt,distance=..5] run function canon:juli/walk_to
scoreboard players add @s dv.timer2 1
execute if score @s dv.timer2 matches 500.. unless entity @a[tag=dv_jtgt,distance=..4] run function canon:casa/move
execute if score @s dv.timer2 matches 900.. run function canon:casa/move
execute if score #m200 dv.clock matches 50 if entity @a[tag=dv_jtgt] if score @s dv.say matches ..0 if predicate canon:azar/1en2 run function canon:casa/idle_line
execute if score #m200 dv.clock matches 100 run function canon:casa/windows
execute if score #m200 dv.clock matches 150 unless entity @a[tag=dv_jtgt] if predicate canon:azar/1en3 run playsound canon:sueno.blanco_eco ambient @a[predicate=canon:en_casa_sueno,distance=..40] ~ ~ ~ 0.6 1
