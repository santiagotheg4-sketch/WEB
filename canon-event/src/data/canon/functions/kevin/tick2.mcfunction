function canon:x/links_follow
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players remove @s[scores={dv.timer2=1..}] dv.timer2 1
execute if score @s dv.timer2 matches 0 run function canon:kevin/pose_reset
tag @a remove dv_wtgt
tag @a[gamemode=!spectator,distance=..64,limit=1,sort=nearest] add dv_wtgt
execute if score @s dv.mode matches 0 run function canon:kevin/m_follow
execute if score @s dv.mode matches 1 if score #m4 dv.clock matches 0 run function canon:x/face
execute if score @s dv.mode matches 2 if score #m4 dv.clock matches 0 run function canon:x/face
tag @a remove dv_wtgt
execute if score @s dv.mode matches 0 unless entity @a[distance=..72] run function canon:kevin/leave
