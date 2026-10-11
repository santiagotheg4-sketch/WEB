scoreboard players set @s dv.mode 1
scoreboard players set @s dv.timer 0
scoreboard players set @s dv.idle 160
function canon:devota/face
tag @s add dv_waving
scoreboard players set @s dv.jeal 40
execute if score #es dv.tmp matches 1 run function canon:devota/greet/1
execute if score #es dv.tmp matches 2 run function canon:devota/greet/2
execute if score #es dv.tmp matches 3 run function canon:devota/greet/3
execute if score #es dv.tmp matches 4 run function canon:devota/greet/4
execute if score #es dv.tmp matches 5 run function canon:devota/greet/5
execute if score #es dv.tmp matches 6 run function canon:devota/greet/6
