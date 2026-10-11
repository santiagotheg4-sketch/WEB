execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players add @s dv.timer 1
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #60 dv.math
execute if score #c dv.tmp matches 0..29 run tag @s add dv_mpeek
execute if score #c dv.tmp matches 30.. run tag @s remove dv_mpeek
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #80 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:miron.respira hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.9
execute if score @s dv.watch matches 12.. run function canon:miron/seen_react
execute if entity @a[tag=dv_wtgt,distance=..8] run function canon:miron/close_react
execute if score @s dv.timer matches 300.. run function canon:miron/gone
