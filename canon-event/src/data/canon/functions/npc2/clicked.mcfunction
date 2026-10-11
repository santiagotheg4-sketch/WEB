# clic en una interacción de la segunda oleada (el jugador tiene dv_talker)
execute if entity @s[tag=dv_nota] at @s run function canon:kevin/bosque/nota_taken
execute if entity @s[tag=dv_cllave] at @s run function canon:kevin/cata/llave_taken
execute if entity @s[tag=dv_creja] at @s run function canon:kevin/cata/reja_used
execute if entity @s[tag=dv_cfoto] at @s run function canon:casa/foto_taken
scoreboard players operation #id dv.tmp = @s dv.id
execute if entity @s[tag=dv_kev_click] as @e[type=zombie,tag=dv_kevin,distance=..6] if score @s dv.id = #id dv.tmp at @s run function canon:kevin/clicked
