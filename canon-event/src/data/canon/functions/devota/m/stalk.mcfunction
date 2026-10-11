execute if score #m2 dv.clock matches 0 run function canon:devota/face
execute if score #d dv.tmp matches ..5 run function canon:devota/start_hunt
execute if score @s dv.mode matches 4 if score #heard dv.tmp matches 1 run function canon:devota/start_hunt
execute if score @s dv.mode matches 4 if score #es dv.tmp matches 6 if score @s dv.timer matches 60.. run function canon:devota/start_hunt
execute if score @s dv.mode matches 4 run function canon:devota/m/stalk2
