scoreboard players set #townmode dv.dev 0
scoreboard players set #tcalm dv.dev -1
scoreboard players add #sane dv.dev 150
execute as @e[type=zombie,tag=dv_devota] at @s if predicate canon:en_pueblo run function canon:rig/vanish
scoreboard players set #cd dv.dev 600
