execute if predicate canon:en_pueblo run tellraw @s {"text":"Son las llaves del descapotable del taller. Súbete al carro con ellas en el inventario.","color":"gray","italic":true}
execute unless predicate canon:en_pueblo unless score @s dv.cool matches 1.. run function canon:car/call
