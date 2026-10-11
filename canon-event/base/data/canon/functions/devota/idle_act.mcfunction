scoreboard players set @s dv.idle 200
execute if predicate canon:azar/50 run scoreboard players add @s dv.idle 100
function canon:devota/clear_acts
scoreboard players set #act dv.tmp 0
execute if score #es dv.tmp matches 4 if predicate canon:azar/1en3 run scoreboard players set #act dv.tmp 9
execute if score #act dv.tmp matches 0 if score #es dv.tmp matches 2..4 unless score #qt dv.dev matches 1.. if predicate canon:azar/1en5 run scoreboard players set #act dv.tmp 8
execute if score #act dv.tmp matches 0 if score #es dv.tmp matches 2..3 if predicate canon:azar/1en6 run scoreboard players set #act dv.tmp 7
execute if score #act dv.tmp matches 0 if score #es dv.tmp matches 2..3 if predicate canon:azar/1en5 run scoreboard players set #act dv.tmp 6
execute if score #act dv.tmp matches 0 if predicate canon:azar/1en4 run scoreboard players set #act dv.tmp 5
execute if score #act dv.tmp matches 0 run scoreboard players set #act dv.tmp 1
execute if score #act dv.tmp matches 1 run function canon:devota/talk_line
execute if score #act dv.tmp matches 5 run function canon:devota/act/hum
execute if score #act dv.tmp matches 6 run function canon:devota/act/sit
execute if score #act dv.tmp matches 7 run function canon:devota/act/gift
execute if score #act dv.tmp matches 8 run function canon:devota/q/ask
execute if score #act dv.tmp matches 9 run function canon:devota/start_ritual
