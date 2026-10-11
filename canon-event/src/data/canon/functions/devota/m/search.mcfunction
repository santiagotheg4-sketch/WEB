execute if score #m2 dv.clock matches 0 run tp @s ~ ~ ~ ~6 ~
execute if score #heard dv.tmp matches 1 run function canon:devota/start_hunt
execute if score @s dv.mode matches 6 if score @s dv.timer matches 140.. run function canon:devota/end_search
