execute unless score #kev dv.dev matches 1 run function canon:rig/despawn
tag @a remove dv_wtgt
execute if entity @s[tag=dv_fstare] run tag @a[tag=dv_kpart,distance=..32,limit=1,sort=nearest] add dv_wtgt
execute if entity @s[tag=dv_fstare] run function canon:x/face
tag @a remove dv_wtgt
