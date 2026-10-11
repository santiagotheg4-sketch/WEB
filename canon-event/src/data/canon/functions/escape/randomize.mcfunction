scoreboard players set #c1 dv.puzzle 0
scoreboard players set #c2 dv.puzzle 0
scoreboard players set #c3 dv.puzzle 0
scoreboard players set #c4 dv.puzzle 0
execute if predicate canon:azar/50 run scoreboard players set #c1 dv.puzzle 1
execute if predicate canon:azar/50 run scoreboard players set #c2 dv.puzzle 1
execute if predicate canon:azar/50 run scoreboard players set #c3 dv.puzzle 1
execute if predicate canon:azar/50 run scoreboard players set #c4 dv.puzzle 1
execute if score #c1 dv.puzzle matches 0 if score #c2 dv.puzzle matches 0 if score #c3 dv.puzzle matches 0 if score #c4 dv.puzzle matches 0 run scoreboard players set #c3 dv.puzzle 1
scoreboard players set #d1 dv.puzzle 1
scoreboard players set #d2 dv.puzzle 1
scoreboard players set #d3 dv.puzzle 1
scoreboard players set #d4 dv.puzzle 1
execute if predicate canon:azar/1en3 run scoreboard players set #d1 dv.puzzle 2
execute if score #d1 dv.puzzle matches 1 if predicate canon:azar/50 run scoreboard players set #d1 dv.puzzle 3
execute if predicate canon:azar/1en3 run scoreboard players set #d2 dv.puzzle 2
execute if score #d2 dv.puzzle matches 1 if predicate canon:azar/50 run scoreboard players set #d2 dv.puzzle 3
execute if predicate canon:azar/1en3 run scoreboard players set #d3 dv.puzzle 2
execute if score #d3 dv.puzzle matches 1 if predicate canon:azar/50 run scoreboard players set #d3 dv.puzzle 3
execute if predicate canon:azar/1en3 run scoreboard players set #d4 dv.puzzle 2
execute if score #d4 dv.puzzle matches 1 if predicate canon:azar/50 run scoreboard players set #d4 dv.puzzle 3
scoreboard players set #seqpos dv.puzzle 0
scoreboard players set #clues dv.puzzle 0
scoreboard players set #poster dv.puzzle 0
scoreboard players set #sol1 dv.puzzle 0
scoreboard players set #sol2 dv.puzzle 0
scoreboard players set #sol3 dv.puzzle 0
scoreboard players set #p_bat dv.parts 0
scoreboard players set #p_gas dv.parts 0
scoreboard players set #p_buj dv.parts 0
scoreboard players set #p_lla dv.parts 0
scoreboard players set #parts dv.parts 0
scoreboard players set #rs_pending dv.puzzle 1
scoreboard players set #car_pend dv.puzzle 1
