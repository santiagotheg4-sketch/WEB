scoreboard players set @s dv.say 900
scoreboard players set #r dv.tmp 0
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
scoreboard players operation #r dv.tmp %= #3 dv.math
execute if score #r dv.tmp matches 0 run tellraw @a[distance=..6] [{"text":"El Farmaceuta: ","color":"#9fd8b0"},{"text":"¿Insomnio? Los somníferos te vuelven invisible a sus oídos.","color":"white","italic":true}]
execute if score #r dv.tmp matches 1 run tellraw @a[distance=..6] [{"text":"El Farmaceuta: ","color":"#9fd8b0"},{"text":"Las pastillas negras no las vendo yo. No me preguntes.","color":"white","italic":true}]
execute if score #r dv.tmp matches 2 run tellraw @a[distance=..6] [{"text":"El Farmaceuta: ","color":"#9fd8b0"},{"text":"Tómate dos analgésicos y no mires atrás.","color":"white","italic":true}]
