clear @s minecraft:paper{canon:{id:"bateria"}} 1
scoreboard players set #p_bat dv.parts 1
scoreboard players add #parts dv.parts 1
playsound minecraft:block.anvil.use neutral @a[distance=..16] ~ ~ ~ 0.6 1.4
scoreboard players operation #pn dv.parts = #p_bat dv.parts
scoreboard players operation #pn dv.parts += #p_gas dv.parts
scoreboard players operation #pn dv.parts += #p_buj dv.parts
scoreboard players operation #pn dv.parts += #p_lla dv.parts
tellraw @a[predicate=canon:en_pueblo] [{"text":"Instalaste la batería en el descapotable. ","color":"#9fd8b0"},{"score":{"name":"#pn","objective":"dv.parts"},"color":"white"},{"text":"/4 piezas","color":"gray"}]
