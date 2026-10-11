scoreboard players remove @s dv.talk 1
scoreboard players set @s dv.talkdec 1200
execute if score @s dv.talk matches 0 run tag @s remove dv_stare
