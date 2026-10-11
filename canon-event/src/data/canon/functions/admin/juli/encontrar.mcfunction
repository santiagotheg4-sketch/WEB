tag @s add dv_santi
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #jstate dv.tmp 2
execute rotated ~ 0 positioned ^ ^ ^3 run function canon:spawn/juli
