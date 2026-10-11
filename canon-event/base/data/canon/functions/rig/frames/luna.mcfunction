scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #8 dv.math
execute if score @s dv.mode matches 1 run scoreboard players set #frame dv.tmp 9
execute if score @s dv.mode matches 2 run scoreboard players set #frame dv.tmp 10
execute if score @s dv.mode matches 4 run scoreboard players set #frame dv.tmp 8
execute if score @s dv.mode matches 5 if score #c dv.tmp matches 0..3 run scoreboard players set #frame dv.tmp 6
execute if score @s dv.mode matches 5 if score #c dv.tmp matches 4..7 run scoreboard players set #frame dv.tmp 7
execute if entity @s[tag=dv_lwalk] if score #c dv.tmp matches 0..3 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_lwalk] if score #c dv.tmp matches 4..7 run scoreboard players set #frame dv.tmp 2
execute if entity @s[tag=dv_lrun] if score #c dv.tmp matches 0..3 run scoreboard players set #frame dv.tmp 3
execute if entity @s[tag=dv_lrun] if score #c dv.tmp matches 4..7 run scoreboard players set #frame dv.tmp 4
execute if entity @s[tag=dv_lbark] run scoreboard players set #frame dv.tmp 5
