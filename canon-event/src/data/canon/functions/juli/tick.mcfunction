scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=interaction,tag=dv_juli_click] if score @s dv.id = #id dv.tmp run tp @s ~ ~ ~
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run tp @s ~ ~2.3 ~
execute as @e[type=marker,tag=dv_jlook] if score @s dv.id = #id dv.tmp run tp @s ~ ~1.55 ~
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:juli/bubble_clear
scoreboard players add @s dv.timer 1
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a if score @s dv.pid = #tgt dv.tmp run tag @s add dv_jtgt
tag @s remove dv_jwalk
execute if score @s dv.state matches 1 run function canon:juli/s_ask
execute if score @s dv.state matches 2 run function canon:juli/s_search
execute if score @s dv.state matches 3 run function canon:juli/s_scene
execute if score @s dv.state matches 4 run function canon:juli/s_dream
execute if score @s dv.state matches 5 run function canon:juli/s_bye
execute if score @s dv.state matches 6 run function canon:casa/juli_tick
tag @a[tag=dv_jtgt] remove dv_jtgt
execute if score #m10 dv.clock matches 0 run particle minecraft:cherry_leaves ~ ~1.6 ~ 0.6 0.8 0.6 0 2 normal
execute if score #m20 dv.clock matches 0 run particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.7 0.4 0.01 1 normal
