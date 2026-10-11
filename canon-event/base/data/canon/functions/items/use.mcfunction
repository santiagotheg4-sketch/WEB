scoreboard players set @s dv.use 0
execute if predicate canon:mano/hueso_deseo run function canon:wish/open
execute if predicate canon:mano/revolver run function canon:items/revolver/use
execute if predicate canon:mano/radio run function canon:items/radio/use
execute if predicate canon:mano/boleto run function canon:travel/use_ticket
execute if predicate canon:mano/llaves run function canon:car/use_keys
execute if predicate canon:mano/linterna unless score @s dv.cool matches 1.. run function canon:items/linterna/use
execute if predicate canon:mano/petalo unless score @s dv.cool matches 1.. run function canon:items/petalo/use
