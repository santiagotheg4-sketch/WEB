tag @a remove dv_wtgt
tag @a[tag=dv_kpart,distance=..80,limit=1,sort=nearest] add dv_wtgt
execute unless score #kev dv.dev matches 3 run function canon:rig/despawn
execute if entity @a[tag=dv_wtgt] run function canon:masa/think
tag @a remove dv_wtgt
