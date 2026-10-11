scoreboard players set @s dv.timer2 0
particle minecraft:cherry_leaves ~ ~1 ~ 0.4 0.9 0.4 0 25 normal
particle minecraft:end_rod ~ ~1 ~ 0.3 0.7 0.3 0.02 8 normal
scoreboard players set #r dv.tmp 0
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 1
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 2
execute if predicate canon:azar/50 run scoreboard players add #r dv.tmp 4
execute if score #r dv.tmp = #jroom dv.dev run scoreboard players add #r dv.tmp 3
scoreboard players operation #r dv.tmp %= #8 dv.math
scoreboard players operation #jroom dv.dev = #r dv.tmp
execute if score #r dv.tmp matches 0 run tp @s @e[type=marker,tag=dv_jroom0,limit=1]
execute if score #r dv.tmp matches 1 run tp @s @e[type=marker,tag=dv_jroom1,limit=1]
execute if score #r dv.tmp matches 2 run tp @s @e[type=marker,tag=dv_jroom2,limit=1]
execute if score #r dv.tmp matches 3 run tp @s @e[type=marker,tag=dv_jroom3,limit=1]
execute if score #r dv.tmp matches 4 run tp @s @e[type=marker,tag=dv_jroom4,limit=1]
execute if score #r dv.tmp matches 5 run tp @s @e[type=marker,tag=dv_jroom5,limit=1]
execute if score #r dv.tmp matches 6 run tp @s @e[type=marker,tag=dv_jroom6,limit=1]
execute if score #r dv.tmp matches 7 run tp @s @e[type=marker,tag=dv_jroom7,limit=1]
execute at @s run particle minecraft:cherry_leaves ~ ~1 ~ 0.4 0.9 0.4 0 25 normal
execute at @s run playsound canon:juli.chime ambient @a[distance=..20] ~ ~ ~ 0.5 1.2
