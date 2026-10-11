scoreboard players operation #ty dv.tmp = #hy dv.tmp
scoreboard players operation #ty dv.tmp -= @s dv.calib
execute store result entity @s transformation.translation[1] float 0.001 run scoreboard players get #ty dv.tmp
