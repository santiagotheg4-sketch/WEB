execute unless entity @a[tag=dv_kpart] run function canon:kevin/bosque/fail
execute as @a[tag=dv_kpart] at @s unless entity @e[type=marker,tag=dv_bosque_c,distance=..120] run tag @s remove dv_kpart
execute if score #m40 dv.clock matches 0 as @e[type=item_display,tag=dv_nota_vis] at @s run particle minecraft:end_rod ~ ~0.4 ~ 0.15 0.3 0.15 0.01 2 normal
execute if score #kt dv.dev matches 100 at @a[tag=dv_kpart,limit=1,sort=random] positioned ^ ^ ^-30 positioned over motion_blocking_no_leaves run function canon:alto/spawn
execute if score #kt dv.dev matches 1920 run playsound canon:music.bosque music @a[tag=dv_kpart] ~ ~ ~ 1 1
execute if score #kt dv.dev matches 3840 run playsound canon:music.bosque music @a[tag=dv_kpart] ~ ~ ~ 1 1
execute as @a[tag=dv_kpart] at @s if predicate canon:azar/1en100 run function canon:kevin/bosque/ambient
execute if score #kt dv.dev matches 6000.. run function canon:kevin/bosque/fail
