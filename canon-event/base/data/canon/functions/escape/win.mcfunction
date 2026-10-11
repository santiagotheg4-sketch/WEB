tag @s add dv_escapa
execute at @s as @a[predicate=canon:en_pueblo,distance=..48,gamemode=!spectator,tag=!dv_escapa] run tag @s add dv_escapa_con
ride @s dismount
execute as @e[type=horse,tag=dv_car_town] at @s run function canon:car/remove
function canon:escape/win_one
tellraw @s {"text":"Te llevaste las llaves del descapotable. Úsalas en cualquier parte (fuera del pueblo) para llamar a tu carro.","color":"#9fd8b0","italic":true}
execute as @a[tag=dv_escapa_con] at @s run function canon:escape/win_companion
tellraw @a[predicate=canon:en_pueblo,tag=!dv_escapa,tag=!dv_escapa_con] [{"selector":"@a[tag=dv_escapa]","color":"#d77a8a"},{"text":" escapó en el descapotable sin ti. Valle Quieto vuelve a cerrarse...","color":"gray","italic":true}]
function canon:escape/randomize
function canon:travel/return
execute as @a[tag=dv_escapa_con] at @s run function canon:travel/return
tag @a remove dv_escapa
tag @a remove dv_escapa_con
