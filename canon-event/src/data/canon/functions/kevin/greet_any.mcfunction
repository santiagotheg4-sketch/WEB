scoreboard players set #k dv.tmp 0
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en4 run function canon:kevin/greet_any/o0
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en3 run function canon:kevin/greet_any/o1
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en2 run function canon:kevin/greet_any/o2
execute if score #k dv.tmp matches 0 run function canon:kevin/greet_any/o3
