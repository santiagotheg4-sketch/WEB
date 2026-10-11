scoreboard players set @s dv.say 900
scoreboard players set #r dv.tmp 0
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
scoreboard players operation #r dv.tmp %= #5 dv.math
execute if score #r dv.tmp matches 0 run tellraw @a[distance=..6] [{"text":"Vagabundo: ","color":"#b8a88a"},{"text":"Ese pueblo no aparece en ningún mapa, ¿sabes?","color":"white","italic":true}]
execute if score #r dv.tmp matches 1 run tellraw @a[distance=..6] [{"text":"Vagabundo: ","color":"#b8a88a"},{"text":"¿Tienes algo de comer? Lo que sea.","color":"white","italic":true}]
execute if score #r dv.tmp matches 2 run tellraw @a[distance=..6] [{"text":"Vagabundo: ","color":"#b8a88a"},{"text":"Yo también pedí un deseo. Mírame ahora.","color":"white","italic":true}]
execute if score #r dv.tmp matches 3 run tellraw @a[distance=..6] [{"text":"Vagabundo: ","color":"#b8a88a"},{"text":"No corras de noche. Ella escucha los pasos.","color":"white","italic":true}]
execute if score #r dv.tmp matches 4 run tellraw @a[distance=..6] [{"text":"Vagabundo: ","color":"#b8a88a"},{"text":"La chica del parque... no le hables.","color":"white","italic":true}]
