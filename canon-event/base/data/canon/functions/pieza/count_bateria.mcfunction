execute store result score #h dv.tmp run clear @s minecraft:paper{canon:{id:"bateria"}} 0
execute if score #h dv.tmp matches 1.. run scoreboard players set #n dv.tmp 1
