kill @e[type=marker,tag=dv_spot]
execute align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["dv_spot"]}
scoreboard players set #ok dv.tmp 1
