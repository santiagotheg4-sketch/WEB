execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #done dv.tmp 0
execute as @a[tag=dv_talker,limit=1] if predicate canon:mano_perro run function canon:luna/take_food
execute if score #done dv.tmp matches 1 run function canon:luna/eat
execute if score #done dv.tmp matches 0 if entity @a[tag=dv_talker,predicate=canon:agachado] run function canon:luna/petted
execute if score #done dv.tmp matches 0 unless entity @a[tag=dv_talker,predicate=canon:agachado] run function canon:luna/advice
