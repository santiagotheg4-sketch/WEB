tag @s add dv_mounting
execute as @e[type=horse,tag=dv_car,distance=..6] if score @s dv.id = #id dv.tmp run ride @e[type=item_display,tag=dv_mounting,limit=1] mount @s
tag @s remove dv_mounting
execute if score @s dv.calib matches 0 run function canon:car/body_first_cal
execute unless score @s dv.calib matches 0 run function canon:car/body_cached
