scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-7 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^3 ^ ^-4 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/greet
scoreboard players set #kevcd dv.dev 300
