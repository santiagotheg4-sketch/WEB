scoreboard players set #lv dv.tmp 0
execute if entity @e[type=zombie,tag=dv_devota,distance=..32] if score #stage dv.dev matches 4.. run scoreboard players set #lv dv.tmp 1
execute if entity @e[type=zombie,tag=dv_diana,distance=..36] run scoreboard players set #lv dv.tmp 1
execute if entity @e[tag=dv_monstruo,distance=..32] run scoreboard players set #lv dv.tmp 1
execute if entity @e[type=zombie,tag=dv_devota,distance=..24,scores={dv.mode=5}] run scoreboard players set #lv dv.tmp 2
execute if entity @e[type=zombie,tag=dv_diana,distance=..24,scores={dv.state=3}] run scoreboard players set #lv dv.tmp 2
execute if entity @e[tag=dv_monstruo,tag=dv_cazando,distance=..24] run scoreboard players set #lv dv.tmp 2
execute if entity @e[type=zombie,tag=dv_mariana,distance=..24,scores={dv.state=3}] run scoreboard players set #lv dv.tmp 2
execute if score #lv dv.tmp matches 2 unless score @s dv.mode matches 3..4 run function canon:luna/alarm_run
execute if score #lv dv.tmp matches 1 if score @s dv.talkcd matches ..0 unless score @s dv.mode matches 3..4 run function canon:luna/alarm_watch
execute if score #lv dv.tmp matches 0 if score @s dv.mode matches 4 run scoreboard players set @s dv.mode 0
execute if score #lv dv.tmp matches 0 if score @s dv.talkcd matches ..0 run function canon:luna/notice
execute if score #lv dv.tmp matches 0 if score #m200 dv.clock matches 14 if entity @e[type=#canon:hostiles,tag=!dv_brain,distance=..10] if predicate canon:azar/50 run function canon:luna/bark_mob
