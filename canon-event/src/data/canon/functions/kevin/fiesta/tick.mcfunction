execute unless entity @e[type=marker,tag=dv_fiesta_c] run function canon:kevin/fiesta/cleanup
execute unless entity @a[tag=dv_kpart] run function canon:kevin/fiesta/cleanup
execute as @a[tag=dv_kpart] at @s unless entity @e[type=marker,tag=dv_fiesta_c,distance=..48] run tag @s remove dv_kpart
execute if score #kt dv.dev matches ..899 if score #m4 dv.clock matches 0 at @e[type=marker,tag=dv_fiesta_c] run function canon:kevin/fiesta/lights
execute if score #kt dv.dev matches ..899 if score #m20 dv.clock matches 0 run function canon:kevin/fiesta/spin
execute if score #kt dv.dev matches 400 run function canon:kevin/fiesta/offer
execute if score #kt dv.dev matches 520 as @e[type=zombie,tag=dv_kevin] run tag @s remove dv_koffer
execute as @a[tag=dv_kpart,tag=dv_kdrug] at @s if score #m40 dv.clock matches 0 run function canon:kevin/fiesta/trip
execute if score #kt dv.dev matches 900 run function canon:kevin/fiesta/wrong
execute if score #kt dv.dev matches 960 at @e[type=marker,tag=dv_fiesta_c] run function canon:kevin/fiesta/miron
execute if score #kt dv.dev matches 1040 run function canon:kevin/fiesta/scream
execute if score #kt dv.dev matches 1080 run function canon:kevin/fiesta/end
