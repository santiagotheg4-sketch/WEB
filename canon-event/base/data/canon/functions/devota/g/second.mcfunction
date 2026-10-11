execute if score #devota dv.cfg matches 1 run function canon:devota/g/run
execute unless score #devota dv.cfg matches 1 as @e[type=zombie,tag=dv_devota] at @s run function canon:devota/leave_now
