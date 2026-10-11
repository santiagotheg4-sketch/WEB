execute as @a[tag=dv_tgt,limit=1] at @s if entity @a[tag=!dv_tgt,distance=..3,gamemode=!spectator] run scoreboard players add @s dv.near 2
execute as @a[tag=dv_tgt,limit=1] at @s unless entity @a[tag=!dv_tgt,distance=..3,gamemode=!spectator] run scoreboard players set @s dv.near 0
execute if entity @a[tag=dv_tgt,scores={dv.near=10..}] run function canon:devota/rival_strike
