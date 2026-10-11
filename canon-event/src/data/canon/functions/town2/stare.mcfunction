tag @s add dv_stared
execute as @e[type=wandering_trader,tag=dv_brain,distance=..32] at @s run tp @s ~ ~ ~ facing entity @a[tag=dv_stared,limit=1] eyes
execute if entity @e[type=wandering_trader,tag=dv_brain,distance=..32] run tellraw @s {"text":"Todos en la calle se detienen. Todos te miran.","color":"#c94a4a","italic":true}
tag @s remove dv_stared
