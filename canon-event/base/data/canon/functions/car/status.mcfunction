data modify storage canon:hud c set value []
data modify storage canon:hud c append value '{"text":"No arranca. Faltan: ","color":"gray"}'
execute unless score #p_bat dv.parts matches 1 run data modify storage canon:hud c append value '{"text":"batería ","color":"#e0b43a"}'
execute unless score #p_gas dv.parts matches 1 run data modify storage canon:hud c append value '{"text":"gasolina ","color":"#e86a4a"}'
execute unless score #p_buj dv.parts matches 1 run data modify storage canon:hud c append value '{"text":"bujías ","color":"#f0ede4"}'
execute unless score #p_lla dv.parts matches 1 run data modify storage canon:hud c append value '{"text":"llaves","color":"#c9ced6"}'
title @s actionbar {"nbt":"c[]","storage":"canon:hud","interpret":true,"separator":""}
