scoreboard players operation #c dv.tmp = #kt dv.dev
scoreboard players operation #c dv.tmp %= #3 dv.math
execute if score #c dv.tmp matches 0 run particle minecraft:dust 1 0.2 0.8 1.6 ~ ~2.5 ~ 4 1.5 4 0 25 force @a[tag=dv_kpart]
execute if score #c dv.tmp matches 1 run particle minecraft:dust 0.2 0.9 1 1.6 ~ ~2.5 ~ 4 1.5 4 0 25 force @a[tag=dv_kpart]
execute if score #c dv.tmp matches 2 run particle minecraft:dust 0.6 1 0.2 1.6 ~ ~2.5 ~ 4 1.5 4 0 25 force @a[tag=dv_kpart]
particle minecraft:end_rod ~ ~6 ~ 2 0.2 2 0.05 3 force @a[tag=dv_kpart]
