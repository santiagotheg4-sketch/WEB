scoreboard players set #met dv.dev 0
scoreboard players set #love dv.dev 0
scoreboard players set #sane dv.dev 1000
scoreboard players set #cd dv.dev 0
execute as @e[type=zombie,tag=dv_devota] at @s run function canon:rig/despawn
tellraw @s {"text":"[Canon Event] La Devota vuelve a ser una desconocida.","color":"dark_gray"}
