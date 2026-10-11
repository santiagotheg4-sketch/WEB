execute store result score #yaw dv.tmp run data get entity @s Rotation[0] 10
scoreboard players add #yaw dv.tmp 3712
scoreboard players operation #yaw dv.tmp /= #225 dv.math
scoreboard players operation #yaw dv.tmp %= #16 dv.math
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^-3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:diana/sign/place_here
kill @e[type=marker,tag=dv_spot]
