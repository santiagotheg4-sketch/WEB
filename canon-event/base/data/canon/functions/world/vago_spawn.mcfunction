scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^ ^ ^-18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/vago_paso
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run tellraw @s {"text":"Oyes una armónica a lo lejos. Alguien está de paso.","color":"#b8a88a","italic":true}
