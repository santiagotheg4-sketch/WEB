scoreboard players set #ty dv.tmp 750
scoreboard players operation #ty dv.tmp -= @s dv.calib
execute store result entity @s transformation.translation[1] float 0.001 run scoreboard players get #ty dv.tmp
