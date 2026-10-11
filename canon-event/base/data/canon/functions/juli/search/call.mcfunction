scoreboard players set #k dv.tmp 0
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en5 run function canon:juli/search/call/o0
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en4 run function canon:juli/search/call/o1
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en3 run function canon:juli/search/call/o2
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en2 run function canon:juli/search/call/o3
execute if score #k dv.tmp matches 0 run function canon:juli/search/call/o4
