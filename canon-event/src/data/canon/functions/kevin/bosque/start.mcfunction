scoreboard players set #kev dv.dev 2
scoreboard players set #kt dv.dev 0
scoreboard players set #knotes dv.dev 0
tag @a[gamemode=!spectator,distance=..32] add dv_kpart
kill @e[type=marker,tag=dv_bosque_c]
summon minecraft:marker ~ ~ ~ {Tags:["dv_bosque_c"]}
execute positioned ~22 ~ ~0 positioned over motion_blocking_no_leaves run function canon:kevin/bosque/nota_spawn
execute positioned ~-20 ~ ~10 positioned over motion_blocking_no_leaves run function canon:kevin/bosque/nota_spawn
execute positioned ~6 ~ ~28 positioned over motion_blocking_no_leaves run function canon:kevin/bosque/nota_spawn
execute positioned ~-8 ~ ~-26 positioned over motion_blocking_no_leaves run function canon:kevin/bosque/nota_spawn
execute positioned ~26 ~ ~-18 positioned over motion_blocking_no_leaves run function canon:kevin/bosque/nota_spawn
execute positioned ~-28 ~ ~-12 positioned over motion_blocking_no_leaves run function canon:kevin/bosque/nota_spawn
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:kevin/bosque/kevin_runs
playsound canon:music.bosque music @a[tag=dv_kpart] ~ ~ ~ 1 1
title @a[tag=dv_kpart] times 10 60 20
title @a[tag=dv_kpart] subtitle {"text":"Encuentra las 6 notas. No lo mires mucho tiempo.","color":"gray","italic":true}
title @a[tag=dv_kpart] title {"text":"EL BOSQUE","color":"#d8d8d8"}
