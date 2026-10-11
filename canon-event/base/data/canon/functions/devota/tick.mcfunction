scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=interaction,tag=dv_dev_click] if score @s dv.id = #id dv.tmp run tp @s ~ ~ ~
execute as @e[type=text_display,tag=dv_dev_bubble] if score @s dv.id = #id dv.tmp run tp @s ~ ~2.3 ~
execute if entity @s[tag=dv_sitting] as @e[type=text_display,tag=dv_dev_bubble] if score @s dv.id = #id dv.tmp at @s run tp @s ~ ~-0.55 ~
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:devota/bubble_clear
scoreboard players operation #tgt dv.tmp = @s dv.target
tag @a remove dv_tgt
execute as @a if score @s dv.pid = #tgt dv.tmp run tag @s add dv_tgt
execute unless entity @a[tag=dv_tgt,distance=..120] run function canon:devota/retarget
execute if entity @a[tag=dv_tgt,distance=..120] run function canon:devota/think
