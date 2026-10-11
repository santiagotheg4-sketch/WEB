scoreboard players remove @s dv.timer2 1
execute if block ^ ^ ^0.6 #canon:pasable if block ^ ^1 ^0.6 #canon:pasable unless block ^ ^-1 ^0.6 #canon:pasable run tp @s ^ ^ ^0.22
execute if score @s dv.timer2 matches ..0 run scoreboard players set @s dv.state 0
