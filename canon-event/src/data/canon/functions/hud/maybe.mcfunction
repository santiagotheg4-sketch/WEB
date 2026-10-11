scoreboard players set #show dv.tmp 0
execute if predicate canon:en_pueblo run scoreboard players set #show dv.tmp 1
execute if entity @e[type=zombie,tag=dv_devota,distance=..64] run scoreboard players set #show dv.tmp 1
execute if score #stage dv.dev matches 4.. if predicate canon:visitable run scoreboard players set #show dv.tmp 1
execute if score @s dv.seen matches 1.. run scoreboard players set #show dv.tmp 1
execute if score #lalert dv.dev matches 1.. if entity @e[type=wolf,tag=dv_luna,distance=..32] run scoreboard players set #show dv.tmp 1
execute if score @s dv.hudon matches 1.. run scoreboard players set #show dv.tmp 1
scoreboard players remove @s[scores={dv.hudon=1..}] dv.hudon 1
execute if score #hud dv.cfg matches 0 run scoreboard players set #show dv.tmp 0
execute if score @s dv.hud matches 0 run scoreboard players set #show dv.tmp 0
execute if score @s dv.debug matches 1 run function canon:admin/debug_bar
execute if score #show dv.tmp matches 1 unless score @s dv.debug matches 1 unless score @s dv.cool matches 1.. run function canon:hud/show
