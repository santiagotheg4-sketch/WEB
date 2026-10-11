execute as @e[type=zombie,tag=dv_devota] at @s run function canon:rig/vanish
scoreboard players set #cd dv.dev 1800
scoreboard players remove #sane dv.dev 150
tellraw @s {"text":"Se fue. Puedes respirar. Pero va a volver dolida.","color":"#9ab8f0","italic":true}
