execute if predicate canon:en_pueblo run tellraw @s {"text":"[Canon Event] Sal del pueblo primero.","color":"dark_gray"}
execute unless predicate canon:en_pueblo run function canon:sueno/enter
