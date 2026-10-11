execute if score @s dv.deseo matches 9 run tellraw @s {"text":"Guardas el hueso. Por ahora.","color":"gray","italic":true}
execute if score @s dv.deseo matches 1..5 run function canon:wish/consume
scoreboard players set @s dv.wish 0
