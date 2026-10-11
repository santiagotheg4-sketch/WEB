tag @s add dv_car_town
scoreboard players set @s dv.car 1
execute if score #parts dv.parts matches 15 run scoreboard players set @s dv.car 2
scoreboard players set @s dv.target 0
