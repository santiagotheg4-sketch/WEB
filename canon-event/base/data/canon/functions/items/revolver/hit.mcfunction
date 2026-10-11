damage @s 12 minecraft:player_attack by @a[tag=dv_shooter,limit=1]
execute at @s run particle minecraft:damage_indicator ~ ~1 ~ 0.2 0.2 0.2 0.1 4 normal
scoreboard players set #ray dv.tmp 999
