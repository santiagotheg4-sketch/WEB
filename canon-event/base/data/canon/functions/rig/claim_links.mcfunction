scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[tag=dv_link,tag=dv_orphan] if score @s dv.id = #id dv.tmp run tag @s remove dv_orphan
