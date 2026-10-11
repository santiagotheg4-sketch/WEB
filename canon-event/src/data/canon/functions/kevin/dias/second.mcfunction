execute store result score #kday dv.tmp run time query day
execute unless score #kday dv.tmp = #kday_last dv.dev run function canon:kevin/dias/new_day
execute if score #kfakecd dv.dev matches 1.. run scoreboard players remove #kfakecd dv.dev 1
execute if score #kfakecd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_kfake] as @a[gamemode=!spectator,predicate=canon:en_superficie,predicate=canon:de_noche,limit=1,sort=random] at @s if predicate canon:azar/1en60 run function canon:kevin/dias/fake_spawn
