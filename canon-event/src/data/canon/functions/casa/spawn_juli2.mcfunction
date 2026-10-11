scoreboard players set #pid dv.tmp 0
scoreboard players set #jstate dv.tmp 6
function canon:spawn/juli
tag @e[type=zombie,tag=dv_juli,distance=..2,limit=1,sort=nearest] add dv_jcasa
scoreboard players set #jroom dv.dev 0
