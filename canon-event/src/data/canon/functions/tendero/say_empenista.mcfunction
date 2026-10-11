scoreboard players set @s dv.say 900
scoreboard players set #r dv.tmp 0
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
scoreboard players operation #r dv.tmp %= #3 dv.math
execute if score #r dv.tmp matches 0 run tellraw @a[distance=..6] [{"text":"El Empeñista: ","color":"#c9a23c"},{"text":"Todo tiene precio. Hasta tu vida.","color":"white","italic":true}]
execute if score #r dv.tmp matches 1 run tellraw @a[distance=..6] [{"text":"El Empeñista: ","color":"#c9a23c"},{"text":"Ese revólver ya disparó antes. No preguntes a quién.","color":"white","italic":true}]
execute if score #r dv.tmp matches 2 run tellraw @a[distance=..6] [{"text":"El Empeñista: ","color":"#c9a23c"},{"text":"Billetes. Solo acepto billetes.","color":"white","italic":true}]
