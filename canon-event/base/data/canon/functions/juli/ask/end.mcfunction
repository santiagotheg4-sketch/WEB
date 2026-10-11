scoreboard players set #near dv.tmp 0
execute if entity @a[tag=dv_santi,distance=..200] run scoreboard players set #near dv.tmp 1
execute if score #near dv.tmp matches 1 run function canon:juli/ask/hint
execute if score #near dv.tmp matches 0 run function canon:juli/ask/later
