execute if entity @a[tag=dv_ltgt,distance=1.6..] run function canon:luna/run
execute if score #m10 dv.clock matches 0 if predicate canon:azar/1en4 run playsound minecraft:entity.wolf.whine neutral @a[distance=..12] ~ ~ ~ 0.6 1.6
execute if score @s dv.timer matches 400.. run scoreboard players set @s dv.mode 0
