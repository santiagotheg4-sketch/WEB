execute if score @s dv.timer matches 40 run tag @s remove dv_waving
execute if score @s dv.timer matches 40 facing entity @a[tag=dv_tgt,limit=1] feet run tp @s ~ ~ ~ ~180 0
execute if score @s dv.timer matches 41.. run function canon:devota/walk_away
execute if score @s dv.timer matches 140.. run function canon:devota/leave_now
execute if score @s dv.timer matches 41.. if score #seen dv.tmp matches 0 if entity @a[tag=dv_tgt,distance=20..] run function canon:devota/leave_now
