tellraw @s {"text":"Todo lo que brilla atrae algo.","color":"gray","italic":true}
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^-7 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/rata
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/rata
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/gato
kill @e[type=marker,tag=dv_spot]
scoreboard players remove #sane dv.dev 30
