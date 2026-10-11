scoreboard players add @s dv.talk 1
scoreboard players set @s dv.talkdec 1200
tag @s add dv_bailando
tag @s remove dv_stare
scoreboard players set @s dv.music 0
execute as @a[tag=dv_talker] run scoreboard players add @s[scores={dv.obs=150..}] dv.obs 10
execute if score @s dv.talk matches 1 run function canon:mariana/t1
execute if score @s dv.talk matches 2 run function canon:mariana/t2
execute if score @s dv.talk matches 3 run function canon:mariana/t3
execute if score @s dv.talk matches 4 run function canon:mariana/t4
execute if score @s dv.talk matches 5 run function canon:mariana/t5
execute if score @s dv.talk matches 6 run function canon:mariana/t6
execute if score @s dv.talk matches 7.. run function canon:mariana/start_kill
