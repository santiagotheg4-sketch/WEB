tag @s add dv_kme
scoreboard players operation #kme dv.tmp = @s dv.id
scoreboard players set #kdup dv.tmp 0
execute as @e[type=zombie,tag=dv_kevin,tag=!dv_kme] if score @s dv.id < #kme dv.tmp run scoreboard players set #kdup dv.tmp 1
tag @s remove dv_kme
execute if score #kdup dv.tmp matches 0 run function canon:kevin/tick2
execute if score #kdup dv.tmp matches 1 run function canon:rig/despawn
