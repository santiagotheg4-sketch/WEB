execute if score #m4 dv.clock matches 0 run function canon:devota/face
execute if score #seen dv.tmp matches 1 run tag @s add dv_waving
execute if score #seen dv.tmp matches 0 run tag @s remove dv_waving
execute if score @s dv.timer matches 1 run function canon:devota/expr/love
execute if entity @a[distance=..6] run function canon:devota/shy
execute if score @s dv.timer2 matches ..0 run function canon:devota/start_leave
