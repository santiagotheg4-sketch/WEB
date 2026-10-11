execute if predicate canon:en_pueblo run tellraw @s {"text":"Ya estás en Valle Quieto. Aquí el boleto no sirve de nada.","color":"gray","italic":true}
execute unless predicate canon:en_pueblo unless score @s dv.travel matches 1.. run function canon:travel/start
