execute if entity @a[tag=dv_ltgt,distance=10..] run function canon:luna/run
execute if entity @a[tag=dv_ltgt,distance=2.6..10] run function canon:luna/walk
execute unless entity @a[tag=dv_ltgt,distance=2.6..] if score #m4 dv.clock matches 0 run function canon:luna/face
execute unless entity @a[tag=dv_ltgt,distance=2.6..] run scoreboard players add @s dv.idle 1
execute if entity @a[tag=dv_ltgt,distance=2.6..] run scoreboard players set @s dv.idle 0
execute if score @s dv.idle matches 100.. run function canon:luna/to_sit
execute if score #m200 dv.clock matches 131 if predicate canon:azar/1en8 run playsound minecraft:entity.wolf.pant neutral @a[distance=..12] ~ ~ ~ 0.5 1.6
