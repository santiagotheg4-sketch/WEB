summon minecraft:marker ~ ~ ~ {Tags:["dv_car_home"]}
execute rotated as @s as @e[type=marker,tag=dv_car_home,distance=..1,limit=1] positioned as @s run tp @s ~ ~ ~ ~ ~
scoreboard players set #car_pend dv.puzzle 1
