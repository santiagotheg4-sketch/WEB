scoreboard players set #go dv.tmp 0
execute if score @s dv.dia matches 600.. run scoreboard players set #go dv.tmp 1
execute if score @s dv.dia matches 300..599 if predicate canon:azar/50 run scoreboard players set #go dv.tmp 1
execute if score @s dv.dia matches 100..299 if predicate canon:azar/1en4 run scoreboard players set #go dv.tmp 1
execute unless score @s dv.dia matches 100.. if predicate canon:azar/1en10 run scoreboard players set #go dv.tmp 1
execute if score @s dv.parcd matches 1.. run scoreboard players set #go dv.tmp 0
execute if score #paralisis dv.cfg matches 0 run scoreboard players set #go dv.tmp 0
scoreboard players operation #pid dv.tmp = @s dv.pid
execute if entity @e[type=zombie,tag=dv_diana] run scoreboard players set #go dv.tmp 0
execute if score #go dv.tmp matches 1 store result score #h dv.tmp run clear @s minecraft:paper{canon:{id:"atrapasuenos"}} 0
execute if score #go dv.tmp matches 1 if score #h dv.tmp matches 1.. run function canon:diana/par/blocked
execute if score #go dv.tmp matches 1 run function canon:diana/par/start
