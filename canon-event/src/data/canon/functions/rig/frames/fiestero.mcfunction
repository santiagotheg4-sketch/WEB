scoreboard players set #frame dv.tmp 0
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #10 dv.math
execute if score #c dv.tmp matches 5..9 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_fstare] run scoreboard players set #frame dv.tmp 2
