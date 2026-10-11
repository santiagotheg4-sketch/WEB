execute unless score @s dv.town matches 1 run function canon:town/arrive
execute if predicate canon:en_carro if entity @s[x=-6,y=0,z=-148,dx=11,dy=200,dz=16] run function canon:escape/try_win
execute unless entity @s[x=-138,y=-20,z=-138,dx=276,dy=320,dz=276] run function canon:town/boundary
execute if entity @s[y=-100,dy=40] run function canon:town/fell
