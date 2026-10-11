scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=marker,tag=dv_dlook] if score @s dv.id = #id dv.tmp run kill @s
function canon:rig/despawn
