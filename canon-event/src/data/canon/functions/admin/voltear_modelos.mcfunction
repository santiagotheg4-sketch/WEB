execute if score #flip dv.cfg matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score #flip dv.cfg matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation #flip dv.cfg = #tg dv.tmp
execute if score #flip dv.cfg matches 1 as @e[type=item_display,tag=dv_ready] run data modify entity @s transformation.right_rotation set value [0f,1f,0f,0f]
execute if score #flip dv.cfg matches 0 as @e[type=item_display,tag=dv_ready] run data modify entity @s transformation.right_rotation set value [0f,0f,0f,1f]
tellraw @s [{"text":"[Canon Event] Modelos volteados: ","color":"dark_gray"},{"score":{"name":"#flip","objective":"dv.cfg"}}]
