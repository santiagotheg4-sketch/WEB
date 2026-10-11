scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^-22 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^10 ^ ^-18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^-10 ^ ^-18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^ ^ ^-14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 rotated ~ 0 positioned ^ ^ ^14 run function canon:util/spot_search
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #dstate dv.tmp 3
tag @s add dv_dtgt
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/diana
tag @s remove dv_dtgt
kill @e[type=marker,tag=dv_spot]
execute as @e[type=zombie,tag=dv_diana,distance=..30] if score @s dv.target = #pid dv.tmp run scoreboard players set @s dv.timer2 600
title @s times 5 50 15
title @s subtitle {"text":"Algo se arrastra hacia ti. Busca la luz.","color":"dark_red","italic":true}
title @s title {"text":" "}
