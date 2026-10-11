scoreboard players set #go dv.tmp 0
execute if predicate canon:azar/1en300 run scoreboard players set #go dv.tmp 1
execute if predicate canon:en_banca_juli if predicate canon:azar/1en20 run scoreboard players set #go dv.tmp 1
execute if score #go dv.tmp matches 1 run function canon:juli/do_ask
