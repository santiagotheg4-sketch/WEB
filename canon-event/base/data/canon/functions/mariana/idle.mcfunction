execute if score @s dv.talk matches 0 if entity @a[distance=..7] run tag @s remove dv_bailando
execute if score @s dv.talk matches 0 unless entity @a[distance=..7] run tag @s add dv_bailando
execute if score @s dv.talk matches 0 if score #m4 dv.clock matches 0 if entity @a[distance=..7] facing entity @p feet run tp @s ~ ~ ~ ~ ~
