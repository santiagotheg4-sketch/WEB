scoreboard players set #kfakecd dv.dev 240
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^22 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^ ^ ^-18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/dias/fake_summon
kill @e[type=marker,tag=dv_spot]
