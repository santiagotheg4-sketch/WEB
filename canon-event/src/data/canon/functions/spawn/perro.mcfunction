scoreboard players set #r dv.tmp 0
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 2
execute if predicate canon:azar/1en4 run scoreboard players set #r dv.tmp 4
execute if score #r dv.tmp matches 0 run function canon:spawn/perro_0
execute if score #r dv.tmp matches 1 run function canon:spawn/perro_1
execute if score #r dv.tmp matches 2 run function canon:spawn/perro_2
execute if score #r dv.tmp matches 3 run function canon:spawn/perro_3
execute if score #r dv.tmp matches 4 run function canon:spawn/perro_4
