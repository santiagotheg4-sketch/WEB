scoreboard players set #r dv.tmp 0
execute if predicate canon:azar/1en3 run scoreboard players set #r dv.tmp 1
execute if score #r dv.tmp matches 0 if predicate canon:azar/50 run scoreboard players set #r dv.tmp 2
execute if score #r dv.tmp matches 0 run function canon:spawn/vago_0
execute if score #r dv.tmp matches 1 run function canon:spawn/vago_1
execute if score #r dv.tmp matches 2 run function canon:spawn/vago_2
