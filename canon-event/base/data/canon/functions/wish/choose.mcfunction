execute unless score @s dv.wish matches 1 run tellraw @s {"text":"No estás sosteniendo ningún deseo.","color":"gray","italic":true}
execute if score @s dv.wish matches 1 run function canon:wish/try
scoreboard players set @s dv.deseo 0
