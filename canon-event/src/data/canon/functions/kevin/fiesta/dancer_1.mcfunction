scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/fiesta/dancer_summon_1
kill @e[type=marker,tag=dv_spot]
