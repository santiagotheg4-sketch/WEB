scoreboard players set @s dv.timer 0
scoreboard players set #ad dv.tmp 18
scoreboard players operation #an dv.tmp = #knotes dv.dev
scoreboard players operation #an dv.tmp *= #2 dv.math
scoreboard players operation #ad dv.tmp -= #an dv.tmp
execute if score #ad dv.tmp matches ..8 at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-8 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute if score #ad dv.tmp matches 9..12 at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-12 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute if score #ad dv.tmp matches 13.. at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-18 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute at @s run playsound canon:alto.pasos hostile @a[tag=dv_wtgt] ~ ~ ~ 0.9 0.8
