scoreboard players set @s dv.say 900
scoreboard players set #r dv.tmp 0
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
scoreboard players operation #r dv.tmp %= #3 dv.math
execute if score #r dv.tmp matches 0 run tellraw @a[distance=..6] [{"text":"La Vidente: ","color":"#b07ac0"},{"text":"Veo un hilo rojo atado a tu muñeca. Del otro lado, alguien tira.","color":"white","italic":true}]
execute if score #r dv.tmp matches 1 run tellraw @a[distance=..6] [{"text":"La Vidente: ","color":"#b07ac0"},{"text":"Cada hueso guarda un solo deseo. Y un precio.","color":"white","italic":true}]
execute if score #r dv.tmp matches 2 run tellraw @a[distance=..6] [{"text":"La Vidente: ","color":"#b07ac0"},{"text":"El amor que se pide no se puede devolver.","color":"white","italic":true}]
