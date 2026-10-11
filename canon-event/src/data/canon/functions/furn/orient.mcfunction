execute store result score #f dv.tmp run data get entity @s Facing
scoreboard players set #yaw4 dv.tmp -1
execute if score #f dv.tmp matches 2 run scoreboard players set #yaw4 dv.tmp 2
execute if score #f dv.tmp matches 3 run scoreboard players set #yaw4 dv.tmp 0
execute if score #f dv.tmp matches 4 run scoreboard players set #yaw4 dv.tmp 1
execute if score #f dv.tmp matches 5 run scoreboard players set #yaw4 dv.tmp 3
execute if score #yaw4 dv.tmp matches -1 run function canon:furn/orient_player
execute if score #yaw4 dv.tmp matches 0 as @e[tag=dv_furn_new,distance=..1.5] at @s run tp @s ~ ~ ~ 0 0
execute if score #yaw4 dv.tmp matches 1 as @e[tag=dv_furn_new,distance=..1.5] at @s run tp @s ~ ~ ~ 90 0
execute if score #yaw4 dv.tmp matches 2 as @e[tag=dv_furn_new,distance=..1.5] at @s run tp @s ~ ~ ~ 180 0
execute if score #yaw4 dv.tmp matches 3 as @e[tag=dv_furn_new,distance=..1.5] at @s run tp @s ~ ~ ~ 270 0
