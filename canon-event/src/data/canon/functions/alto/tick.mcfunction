tag @s remove dv_xwalk
tag @a remove dv_wtgt
tag @a remove dv_lookers
tag @a[tag=dv_kpart,distance=..160,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_kpart] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:alto/vanish
execute if entity @a[tag=dv_wtgt] run function canon:alto/think
tag @a remove dv_wtgt
tag @a remove dv_lookers
