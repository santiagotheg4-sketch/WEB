scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_jwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_jwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if entity @s[tag=dv_jreach] run scoreboard players set #frame dv.tmp 3
execute if entity @s[tag=dv_jfloat] run scoreboard players set #frame dv.tmp 4
