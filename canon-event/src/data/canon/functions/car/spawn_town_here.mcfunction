scoreboard players set #car_pend dv.puzzle 0
function canon:car/summon_core
execute as @e[type=horse,tag=dv_car,distance=..1,limit=1,sort=nearest] run function canon:car/town
execute rotated as @s as @e[type=horse,tag=dv_car_town,distance=..1,limit=1] positioned as @s run tp @s ~ ~ ~ ~ ~
