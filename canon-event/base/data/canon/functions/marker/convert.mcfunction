execute if entity @s[tag=dv_mk_gato] run function canon:spawn/gato
execute if entity @s[tag=dv_mk_perro] run function canon:spawn/perro
execute if entity @s[tag=dv_mk_cuervo] run function canon:spawn/cuervo
execute if entity @s[tag=dv_mk_rata] run function canon:spawn/rata
execute if entity @s[tag=dv_mk_vago] run function canon:spawn/vago
execute if entity @s[tag=dv_mk_mariana] run summon minecraft:marker ~ ~ ~ {Tags:["dv_home_mari"]}
execute if entity @s[tag=dv_mk_vidente] run function canon:spawn/vidente
execute if entity @s[tag=dv_mk_farmaceuta] run function canon:spawn/farmaceuta
execute if entity @s[tag=dv_mk_empenista] run function canon:spawn/empenista
execute if entity @s[tag=dv_mk_pieza_bateria] run function canon:pieza/init_bateria
execute if entity @s[tag=dv_mk_pieza_gasolina] run function canon:pieza/init_gasolina
execute if entity @s[tag=dv_mk_pieza_bujias] run function canon:pieza/init_bujias
execute if entity @s[tag=dv_mk_pieza_llaves] run function canon:pieza/init_llaves
execute if entity @s[tag=dv_mk_pieza_fusible] run function canon:pieza/init_fusible
execute if entity @s[tag=dv_mk_carro_pueblo] run function canon:car/init_home
execute rotated as @s as @e[tag=dv_brain,distance=..0.6,limit=1,sort=nearest] positioned as @s run tp @s ~ ~ ~ ~ ~
scoreboard players set @e[type=marker,tag=dv_home_mari,distance=..0.5] dv.timer 0
kill @s
