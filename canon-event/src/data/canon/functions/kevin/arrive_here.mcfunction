scoreboard players set #ok dv.tmp 0
execute unless entity @e[type=zombie,tag=dv_kevin] positioned ^ ^ ^3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/summon
kill @e[type=marker,tag=dv_spot]
