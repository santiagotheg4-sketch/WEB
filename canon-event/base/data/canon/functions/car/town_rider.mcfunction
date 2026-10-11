execute unless score #p_bat dv.parts matches 1 store result score #h dv.tmp run clear @s minecraft:paper{canon:{id:"bateria"}} 0
execute unless score #p_bat dv.parts matches 1 if score #h dv.tmp matches 1.. run function canon:car/install_bateria
scoreboard players set #h dv.tmp 0
execute unless score #p_gas dv.parts matches 1 store result score #h dv.tmp run clear @s minecraft:paper{canon:{id:"gasolina"}} 0
execute unless score #p_gas dv.parts matches 1 if score #h dv.tmp matches 1.. run function canon:car/install_gasolina
scoreboard players set #h dv.tmp 0
execute unless score #p_buj dv.parts matches 1 store result score #h dv.tmp run clear @s minecraft:paper{canon:{id:"bujias"}} 0
execute unless score #p_buj dv.parts matches 1 if score #h dv.tmp matches 1.. run function canon:car/install_bujias
scoreboard players set #h dv.tmp 0
execute unless score #p_lla dv.parts matches 1 store result score #h dv.tmp run clear @s minecraft:carrot_on_a_stick{canon:{id:"llaves"}} 0
execute unless score #p_lla dv.parts matches 1 if score #h dv.tmp matches 1.. run function canon:car/install_llaves
scoreboard players set #h dv.tmp 0
execute if score #parts dv.parts matches 15 as @e[type=horse,tag=dv_car_town,distance=..2] if score @s dv.car matches 1 run function canon:car/repair
execute if score #parts dv.parts matches ..14 if score #m10 dv.clock matches 0 run function canon:car/status
