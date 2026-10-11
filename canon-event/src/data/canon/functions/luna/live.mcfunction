scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=interaction,tag=dv_luna_click] if score @s dv.id = #id dv.tmp run tp @s ~ ~ ~
execute as @e[type=text_display,tag=dv_luna_bubble] if score @s dv.id = #id dv.tmp run tp @s ~ ~1.25 ~
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:luna/bubble_clear
scoreboard players add @s dv.timer 1
scoreboard players remove @s[scores={dv.talkcd=1..}] dv.talkcd 1
scoreboard players remove @s[scores={dv.jeal=1..}] dv.jeal 1
tag @s remove dv_lwalk
tag @s remove dv_lrun
tag @a remove dv_ltgt
tag @a[gamemode=!spectator,distance=..80,limit=1,sort=nearest] add dv_ltgt
execute unless entity @a[tag=dv_ltgt] run scoreboard players set @s dv.mode 1
execute if entity @a[tag=dv_ltgt,distance=40..] run function canon:luna/catch_up
execute if score @s dv.mode matches 0 run function canon:luna/m/follow
execute if score @s dv.mode matches 1 run function canon:luna/m/sit
execute if score @s dv.mode matches 2 run function canon:luna/m/sleep
execute if score @s dv.mode matches 3 run function canon:luna/m/alert
execute if score @s dv.mode matches 4 run function canon:luna/m/hide
execute if score @s dv.mode matches 5 run function canon:luna/m/happy
execute if score @s dv.mode matches 6 run function canon:luna/m/sad
execute if score #m20 dv.clock matches 14 run function canon:luna/scan
