function canon:car/summon_core
execute as @e[type=horse,tag=dv_car,distance=..1,limit=1,sort=nearest] run function canon:car/own
