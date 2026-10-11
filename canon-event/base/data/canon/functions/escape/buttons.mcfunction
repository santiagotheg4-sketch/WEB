scoreboard players set #now1 dv.tmp 0
execute if block -32 65 -40 minecraft:crimson_button[powered=true] run scoreboard players set #now1 dv.tmp 1
execute if score #now1 dv.tmp matches 1 unless score #prev1 dv.puzzle matches 1 run function canon:escape/press1
scoreboard players operation #prev1 dv.puzzle = #now1 dv.tmp
scoreboard players set #now2 dv.tmp 0
execute if block -34 65 -40 minecraft:warped_button[powered=true] run scoreboard players set #now2 dv.tmp 1
execute if score #now2 dv.tmp matches 1 unless score #prev2 dv.puzzle matches 1 run function canon:escape/press2
scoreboard players operation #prev2 dv.puzzle = #now2 dv.tmp
scoreboard players set #now3 dv.tmp 0
execute if block -36 65 -40 minecraft:birch_button[powered=true] run scoreboard players set #now3 dv.tmp 1
execute if score #now3 dv.tmp matches 1 unless score #prev3 dv.puzzle matches 1 run function canon:escape/press3
scoreboard players operation #prev3 dv.puzzle = #now3 dv.tmp
