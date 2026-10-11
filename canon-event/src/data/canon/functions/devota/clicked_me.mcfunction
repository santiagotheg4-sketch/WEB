function canon:devota/g/es
execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #given dv.tmp 0
execute as @a[tag=dv_talker,limit=1] if predicate canon:mano_flor run function canon:devota/give_flower
execute if score #given dv.tmp matches 0 as @a[tag=dv_talker,limit=1] if predicate canon:mano_comida run function canon:devota/give_food
execute if score #given dv.tmp matches 1 run function canon:devota/thanks
execute if score #given dv.tmp matches 0 run function canon:devota/talked
