tag @a remove dv_dtgt
tag @a[distance=..64,gamemode=!spectator,limit=1,sort=nearest] add dv_dtgt
execute if entity @a[tag=dv_dtgt] run scoreboard players operation @s dv.target = @a[tag=dv_dtgt,limit=1] dv.pid
