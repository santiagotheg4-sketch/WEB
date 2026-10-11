scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #8 dv.math
execute if score @s dv.state matches 2 if score #c dv.tmp matches 0..3 run scoreboard players set #frame dv.tmp 5
execute if score @s dv.state matches 2 if score #c dv.tmp matches 4..7 run scoreboard players set #frame dv.tmp 6
execute if score @s dv.state matches 3 if score #c dv.tmp matches 0..3 run scoreboard players set #frame dv.tmp 7
execute if score @s dv.state matches 3 if score #c dv.tmp matches 4..7 run scoreboard players set #frame dv.tmp 8
execute if score @s dv.state matches 5 run scoreboard players set #frame dv.tmp 3
execute if score @s dv.state matches 6 run scoreboard players set #frame dv.tmp 5
execute if score @s dv.state matches 4 if entity @s[tag=dv_djitter] if score #c dv.tmp matches 0..3 run scoreboard players set #frame dv.tmp 5
execute if score @s dv.state matches 4 if entity @s[tag=dv_djitter] if score #c dv.tmp matches 4..7 run scoreboard players set #frame dv.tmp 6
execute if score @s dv.state matches 4 if entity @s[tag=dv_dreach] run scoreboard players set #frame dv.tmp 3
execute if score @s dv.state matches 7 if score #c dv.tmp matches 0..3 run scoreboard players set #frame dv.tmp 1
execute if score @s dv.state matches 7 if score #c dv.tmp matches 4..7 run scoreboard players set #frame dv.tmp 2
