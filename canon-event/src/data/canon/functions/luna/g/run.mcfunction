scoreboard players remove #lalert dv.dev 20
execute if score #lalert dv.dev matches ..-1 run scoreboard players set #lalert dv.dev 0
scoreboard players set #lok dv.tmp 0
execute as @a[predicate=!canon:sin_luna,gamemode=!spectator] at @s if entity @e[type=wolf,tag=dv_luna,distance=..64] run scoreboard players set #lok dv.tmp 1
execute unless entity @a[predicate=!canon:sin_luna,gamemode=!spectator] run scoreboard players set #lok dv.tmp 1
execute if score #lok dv.tmp matches 1 run scoreboard players set #lmiss dv.dev 0
execute if score #lok dv.tmp matches 0 run scoreboard players add #lmiss dv.dev 1
execute if score #lmiss dv.dev matches 6.. as @r[predicate=!canon:sin_luna,gamemode=!spectator] at @s run function canon:luna/g/come
