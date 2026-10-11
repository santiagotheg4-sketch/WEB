tag @s add dv_kdrug
scoreboard players set #kdrunk dv.dev 1
effect give @s minecraft:nausea 40 0 true
effect give @s minecraft:speed 30 1 true
playsound canon:kevin.drugged music @s ~ ~ ~ 1 1
tellraw @s {"text":"Sabe a chicle y a pilas. Las luces empiezan a respirar.","color":"#ff5ad1","italic":true}
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/laugh
