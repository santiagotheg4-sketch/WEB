execute store result score #h dv.tmp run clear @s minecraft:paper{canon:{id:"pilas"}} 0
execute if score #h dv.tmp matches 1.. run function canon:items/linterna/recharge_do
