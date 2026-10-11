scoreboard players operation #pid dv.tmp = @s dv.pid
tellraw @s {"text":"[Canon Event] Galería de criaturas frente a ti.","color":"dark_gray"}
execute rotated ~ 0 positioned ^-10.0 ^ ^7 run function canon:spawn/mariana
execute rotated ~ 0 positioned ^-7.5 ^ ^7 run function canon:spawn/gato
execute rotated ~ 0 positioned ^-5.0 ^ ^7 run function canon:spawn/perro
execute rotated ~ 0 positioned ^-2.5 ^ ^7 run function canon:spawn/cuervo
execute rotated ~ 0 positioned ^0.0 ^ ^7 run function canon:spawn/rata
execute rotated ~ 0 positioned ^2.5 ^ ^7 run function canon:spawn/vago
execute rotated ~ 0 positioned ^5.0 ^ ^7 run function canon:spawn/vidente
execute rotated ~ 0 positioned ^7.5 ^ ^7 run function canon:spawn/farmaceuta
execute rotated ~ 0 positioned ^10.0 ^ ^7 run function canon:spawn/empenista
execute rotated ~ 0 positioned ^ ^ ^12 run function canon:car/spawn_player
