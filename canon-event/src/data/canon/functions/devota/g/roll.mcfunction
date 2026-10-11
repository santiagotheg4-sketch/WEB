scoreboard players set #go dv.tmp 0
execute if score #stage dv.dev matches 0 if predicate canon:azar/1en1500 run scoreboard players set #go dv.tmp 1
execute if score #stage dv.dev matches 1 if predicate canon:azar/1en600 run scoreboard players set #go dv.tmp 1
execute if score #stage dv.dev matches 2 if predicate canon:azar/1en400 run scoreboard players set #go dv.tmp 1
execute if score #stage dv.dev matches 3 if predicate canon:azar/1en250 run scoreboard players set #go dv.tmp 1
execute if score #stage dv.dev matches 4 if predicate canon:azar/1en150 run scoreboard players set #go dv.tmp 1
execute if score #stage dv.dev matches 5 if predicate canon:azar/1en60 run scoreboard players set #go dv.tmp 1
execute if score #stage dv.dev matches 6 if predicate canon:azar/1en20 run scoreboard players set #go dv.tmp 1
execute if score #townmode dv.dev matches 1 run scoreboard players set #go dv.tmp 1
execute if score #go dv.tmp matches 1 if score #stage dv.dev matches 0 unless score #townmode dv.dev matches 1 as @a[tag=dv_focus,limit=1] at @s run function canon:devota/visit/first
execute if score #go dv.tmp matches 1 unless score #stage dv.dev matches 0 as @a[tag=dv_focus,limit=1] at @s run function canon:devota/visit/start
execute if score #go dv.tmp matches 1 if score #stage dv.dev matches 0 if score #townmode dv.dev matches 1 as @a[tag=dv_focus,limit=1] at @s run function canon:devota/visit/start
