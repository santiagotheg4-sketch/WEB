tag @a remove dv_jtgt
tag @a[predicate=canon:en_sueno,distance=..24,limit=1,sort=nearest,tag=dv_santi] add dv_jtgt
execute unless entity @a[tag=dv_jtgt] run tag @a[predicate=canon:en_sueno,distance=..24,limit=1,sort=nearest] add dv_jtgt
execute if entity @a[tag=dv_jtgt,distance=4.5..] run function canon:juli/walk_to
execute if entity @a[tag=dv_jtgt,distance=..4.5] if score #m4 dv.clock matches 0 run function canon:juli/face
execute if score #m200 dv.clock matches 77 if entity @a[tag=dv_jtgt] if score @s dv.say matches ..0 if predicate canon:azar/1en3 run function canon:juli/dream/idle
execute unless entity @a[tag=dv_jtgt] if entity @s[distance=12..] run function canon:juli/dream/home
