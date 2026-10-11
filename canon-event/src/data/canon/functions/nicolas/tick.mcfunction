function canon:x/links_follow
tag @s remove dv_xwalk
tag @s remove dv_nreach
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
scoreboard players operation #tgt dv.tmp = @s dv.target
tag @a remove dv_wtgt
execute as @a[distance=..48,gamemode=!spectator] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
scoreboard players add @s dv.timer 1
scoreboard players set #ngo dv.tmp 0
execute unless entity @a[tag=dv_wtgt] run scoreboard players set #ngo dv.tmp 1
execute if entity @a[tag=dv_wtgt,y=56,dy=400] run scoreboard players set #ngo dv.tmp 1
execute if score @s dv.timer matches 1400.. run scoreboard players set #ngo dv.tmp 1
execute if score #ngo dv.tmp matches 0 run function canon:nicolas/hunt
execute if score #ngo dv.tmp matches 1 run function canon:nicolas/leave
tag @a remove dv_wtgt
