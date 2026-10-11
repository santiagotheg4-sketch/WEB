execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
execute as @e[type=zombie,tag=dv_kfake] at @s run function canon:rig/despawn
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/abort
