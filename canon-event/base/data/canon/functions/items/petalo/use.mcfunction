execute if predicate canon:en_pueblo run title @s actionbar {"text":"Aquí no se puede soñar.","color":"gray"}
execute if predicate canon:en_sueno run title @s actionbar {"text":"Ya estás soñando.","color":"#f2a7c3"}
execute unless predicate canon:en_pueblo unless predicate canon:en_sueno run function canon:items/petalo/go
scoreboard players set @s dv.cool 20
