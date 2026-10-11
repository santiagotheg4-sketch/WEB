scoreboard players set #lmiss dv.dev 0
scoreboard players add #lgen dv.dev 1
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^1.5 ^ ^-2 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ~ ~ ~ run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:spawn/luna
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 unless score #lmet dv.dev matches 1 run function canon:luna/g/first
execute if score #ok dv.tmp matches 1 if score #lmet dv.dev matches 1 as @e[type=wolf,tag=dv_luna,distance=..6,limit=1] at @s run function canon:luna/found_you
