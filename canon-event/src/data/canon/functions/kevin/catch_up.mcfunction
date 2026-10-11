scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 as @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] at @e[type=marker,tag=dv_spot,limit=1] run tp @s ~ ~ ~
kill @e[type=marker,tag=dv_spot]
