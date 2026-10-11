scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=interaction,tag=dv_mari_click,distance=..40] if score @s dv.id = #id dv.tmp run tp @s ~ ~ ~
execute as @e[type=text_display,tag=dv_mari_bubble,distance=..40] if score @s dv.id = #id dv.tmp run tp @s ~ ~2.25 ~
scoreboard players remove @s[scores={dv.timer=1..}] dv.timer 1
execute if score @s dv.timer matches 0 if entity @s[tag=dv_has_bubble] run function canon:mariana/bubble_clear
execute if score @s dv.talk matches 1..6 run scoreboard players remove @s dv.talkdec 1
execute if score @s dv.talk matches 1..6 if score @s dv.talkdec matches ..0 run function canon:mariana/calm_down
execute if score @s dv.state matches 1 run function canon:mariana/step_away
execute if score @s dv.state matches 3 run function canon:mariana/chase
execute if score @s dv.state matches 0 run function canon:mariana/idle
scoreboard players remove @s[scores={dv.music=1..}] dv.music 1
execute if entity @s[tag=dv_bailando] if score @s dv.music matches 0 unless score @s dv.state matches 3 run function canon:mariana/music
