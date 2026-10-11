execute unless score @s dv.bat matches -999999..999999 run scoreboard players set @s dv.bat 6000
execute if score @s dv.lint matches 1 run function canon:items/linterna/off
execute unless score @s dv.lint matches 1 if score @s dv.bat matches 1.. run function canon:items/linterna/on
execute unless score @s dv.lint matches 1 if score @s dv.bat matches ..0 run title @s actionbar {"text":"Sin pilas.","color":"gray"}
scoreboard players set @s dv.cool 6
