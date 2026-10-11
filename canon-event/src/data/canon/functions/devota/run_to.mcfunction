tag @s add dv_walking
tag @s remove dv_sitting
execute facing entity @a[tag=dv_tgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.26 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
