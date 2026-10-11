scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #has dv.tmp 0
execute if entity @e[type=zombie,tag=dv_diana] run scoreboard players set #has dv.tmp 1
execute if score #has dv.tmp matches 0 if entity @s[tag=dv_dnext] run function canon:diana/ev/behind
execute if score #has dv.tmp matches 0 unless entity @s[tag=dv_dnext] if predicate canon:azar/1en6 run function canon:diana/event
tag @s remove dv_dnext
