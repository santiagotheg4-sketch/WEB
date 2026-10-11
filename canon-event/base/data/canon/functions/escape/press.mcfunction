scoreboard players set #exp dv.tmp 0
execute if score #seqpos dv.puzzle matches 0 run scoreboard players operation #exp dv.tmp = #d1 dv.puzzle
execute if score #seqpos dv.puzzle matches 1 run scoreboard players operation #exp dv.tmp = #d2 dv.puzzle
execute if score #seqpos dv.puzzle matches 2 run scoreboard players operation #exp dv.tmp = #d3 dv.puzzle
execute if score #seqpos dv.puzzle matches 3 run scoreboard players operation #exp dv.tmp = #d4 dv.puzzle
execute if score #pressed dv.tmp = #exp dv.tmp run scoreboard players add #seqpos dv.puzzle 1
execute unless score #pressed dv.tmp = #exp dv.tmp run function canon:escape/press_wrong
execute if score #seqpos dv.puzzle matches 4 if score #sol2 dv.puzzle matches 0 run function canon:escape/solve2
