execute unless entity @a[tag=dv_jtgt,distance=..12] run function canon:juli/scene_abort
execute if score @s dv.state matches 3 run function canon:juli/scene_run
