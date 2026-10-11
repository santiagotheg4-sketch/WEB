scoreboard players set @s dv.state 3
scoreboard players set @s dv.timer 0
tag @s remove dv_jwalk
scoreboard players operation #pid dv.tmp = @s dv.target
execute as @a[tag=dv_santi,distance=..8,limit=1,sort=nearest] run scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players operation @s dv.target = #pid dv.tmp
tag @a remove dv_jtgt
execute as @a if score @s dv.pid = #pid dv.tmp run tag @s add dv_jtgt
execute as @a[tag=dv_jtgt] run function canon:juli/scene/lock
