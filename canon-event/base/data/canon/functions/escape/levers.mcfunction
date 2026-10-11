scoreboard players set #m dv.tmp 0
execute if score #c1 dv.puzzle matches 1 if block 6 59 -34 minecraft:lever[powered=true] run scoreboard players add #m dv.tmp 1
execute if score #c1 dv.puzzle matches 0 if block 6 59 -34 minecraft:lever[powered=false] run scoreboard players add #m dv.tmp 1
execute if score #c2 dv.puzzle matches 1 if block 4 59 -34 minecraft:lever[powered=true] run scoreboard players add #m dv.tmp 1
execute if score #c2 dv.puzzle matches 0 if block 4 59 -34 minecraft:lever[powered=false] run scoreboard players add #m dv.tmp 1
execute if score #c3 dv.puzzle matches 1 if block 2 59 -34 minecraft:lever[powered=true] run scoreboard players add #m dv.tmp 1
execute if score #c3 dv.puzzle matches 0 if block 2 59 -34 minecraft:lever[powered=false] run scoreboard players add #m dv.tmp 1
execute if score #c4 dv.puzzle matches 1 if block 0 59 -34 minecraft:lever[powered=true] run scoreboard players add #m dv.tmp 1
execute if score #c4 dv.puzzle matches 0 if block 0 59 -34 minecraft:lever[powered=false] run scoreboard players add #m dv.tmp 1
execute if score #m dv.tmp matches 4 if score #sol1 dv.puzzle matches 0 run function canon:escape/solve1
