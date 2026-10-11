scoreboard players operation #es dv.tmp = #stage dv.dev
execute if score #townmode dv.dev matches 1 if predicate canon:en_pueblo if score #es dv.tmp matches ..4 run scoreboard players set #es dv.tmp 5
execute if score #es dv.tmp matches 0 run scoreboard players set #es dv.tmp 1
