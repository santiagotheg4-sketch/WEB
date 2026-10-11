scoreboard players set #lit dv.tmp 0
execute as @a[tag=dv_dtgt,limit=1] at @s if predicate canon:iluminado run scoreboard players set #lit dv.tmp 1
execute if score #lit dv.tmp matches 0 run function canon:diana/hunt_step
execute if score #lit dv.tmp matches 1 if entity @a[tag=dv_dtgt,distance=7..] run function canon:diana/hunt_step
execute if score #lit dv.tmp matches 1 unless entity @a[tag=dv_dtgt,distance=7..] run function canon:diana/hunt_circle
execute if entity @a[tag=dv_dtgt,distance=40..] run function canon:diana/hunt_blink
