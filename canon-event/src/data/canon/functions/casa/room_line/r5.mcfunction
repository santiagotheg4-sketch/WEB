scoreboard players set #k dv.tmp 0
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en3 run function canon:casa/room_line/r5/o0
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en2 run function canon:casa/room_line/r5/o1
execute if score #k dv.tmp matches 0 run function canon:casa/room_line/r5/o2
