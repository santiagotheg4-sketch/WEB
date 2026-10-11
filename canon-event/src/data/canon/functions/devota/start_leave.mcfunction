scoreboard players set @s dv.mode 3
scoreboard players set @s dv.timer 0
function canon:devota/clear_acts
function canon:devota/face
execute if score #es dv.tmp matches 1 run function canon:devota/bye/1
execute if score #es dv.tmp matches 2 run function canon:devota/bye/2
execute if score #es dv.tmp matches 3 run function canon:devota/bye/3
execute if score #es dv.tmp matches 4 run function canon:devota/bye/4
execute if score #es dv.tmp matches 5 run function canon:devota/bye/5
execute if score #es dv.tmp matches 6 run function canon:devota/bye/6
