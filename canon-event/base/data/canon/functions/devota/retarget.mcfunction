tag @a remove dv_tgt
tag @a[distance=..64,gamemode=!spectator,limit=1,sort=nearest] add dv_tgt
execute if entity @a[tag=dv_tgt] run scoreboard players operation @s dv.target = @a[tag=dv_tgt,limit=1] dv.pid
execute unless entity @a[tag=dv_tgt] run function canon:devota/leave_now
