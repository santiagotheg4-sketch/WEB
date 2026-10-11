scoreboard players set #kprog dv.dev 5
scoreboard players set #kdays dv.dev 0
scoreboard players set #kevcd dv.dev 0
execute as @e[type=zombie,tag=dv_kfake] at @s run function canon:rig/despawn
execute as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s run function canon:kevin/dias/return_here
