scoreboard players set #p dv.tmp 12
execute if score @s dv.talk matches 1 run scoreboard players set #p dv.tmp 10
execute if score @s dv.talk matches 2 run scoreboard players set #p dv.tmp 8
execute if score @s dv.talk matches 3 run scoreboard players set #p dv.tmp 6
execute if score @s dv.talk matches 4.. run scoreboard players set #p dv.tmp 4
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp /= #p dv.tmp
scoreboard players operation #c dv.tmp %= #4 dv.math
execute if score #c dv.tmp matches 0 run scoreboard players set #frame dv.tmp 3
execute if score #c dv.tmp matches 1 run scoreboard players set #frame dv.tmp 5
execute if score #c dv.tmp matches 2 run scoreboard players set #frame dv.tmp 4
execute if score #c dv.tmp matches 3 run scoreboard players set #frame dv.tmp 6
scoreboard players operation #r dv.tmp = @s dv.anim
scoreboard players operation #r dv.tmp %= #p dv.tmp
execute if score #r dv.tmp matches 0 run function canon:mariana/sway
