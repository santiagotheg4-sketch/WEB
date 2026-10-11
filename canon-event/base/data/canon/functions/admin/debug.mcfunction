execute if score @s dv.debug matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score @s dv.debug matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation @s dv.debug = #tg dv.tmp
tellraw @s [{"text":"[Canon Event] Depuración: ","color":"dark_gray"},{"score":{"name":"@s","objective":"dv.debug"}}]
