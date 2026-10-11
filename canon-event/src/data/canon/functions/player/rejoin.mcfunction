scoreboard players set @s dv.leave 0
scoreboard players set @s dv.travel 0
effect clear @s minecraft:blindness
effect clear @s minecraft:slowness
execute if score @s dv.par matches 1.. run function canon:diana/par/release
execute if score @s dv.escena matches 1.. run function canon:juli/scene/unlock
execute if predicate canon:en_sueno run scoreboard players set @s dv.sfase 0
