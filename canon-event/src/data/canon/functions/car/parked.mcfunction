execute if entity @s[tag=dv_moving] run function canon:car/stop
execute as @e[type=item_display,tag=dv_carbody,distance=..6] if score @s dv.id = #id dv.tmp run tp @s ~ ~ ~ ~ 0
