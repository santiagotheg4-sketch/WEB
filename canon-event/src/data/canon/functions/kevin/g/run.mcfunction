execute if score #kprog dv.dev matches 4 run function canon:kevin/dias/second
execute if score #kevcd dv.dev matches ..0 unless score #kprog dv.dev matches 4 unless score #kev dv.dev matches 1.. unless entity @e[type=zombie,tag=dv_kevin] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:azar/1en40 run function canon:kevin/arrive
