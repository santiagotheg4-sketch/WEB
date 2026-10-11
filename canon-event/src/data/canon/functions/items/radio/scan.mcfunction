scoreboard players set @s dv.cool 30
playsound canon:items.radio_static player @s ~ ~ ~ 0.8 1
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #rd dv.tmp 0
execute as @e[type=zombie,tag=dv_devota,distance=..64] if score @s dv.target = #pid dv.tmp run scoreboard players set #rd dv.tmp 1
execute as @e[type=zombie,tag=dv_devota,distance=..32] if score @s dv.target = #pid dv.tmp run scoreboard players set #rd dv.tmp 2
execute as @e[type=zombie,tag=dv_devota,distance=..16] if score @s dv.target = #pid dv.tmp run scoreboard players set #rd dv.tmp 3
execute as @e[type=zombie,tag=dv_devota,distance=..8] if score @s dv.target = #pid dv.tmp run scoreboard players set #rd dv.tmp 4
execute if score #rd dv.tmp matches 0 run title @s actionbar [{"text":"Radio: ","color":"gray"},{"text":"▯▯▯▯ ","color":"dark_gray"},{"text":"silencio","color":"gray","italic":true}]
execute if score #rd dv.tmp matches 1 run title @s actionbar [{"text":"Radio: ","color":"gray"},{"text":"▮","color":"#d77a8a"},{"text":"▯▯▯ ","color":"dark_gray"},{"text":"lejos","color":"gray","italic":true}]
execute if score #rd dv.tmp matches 2 run title @s actionbar [{"text":"Radio: ","color":"gray"},{"text":"▮▮","color":"#d77a8a"},{"text":"▯▯ ","color":"dark_gray"},{"text":"cerca","color":"gray","italic":true}]
execute if score #rd dv.tmp matches 3 run title @s actionbar [{"text":"Radio: ","color":"gray"},{"text":"▮▮▮","color":"#c43a4a"},{"text":"▯ ","color":"dark_gray"},{"text":"muy cerca","color":"gray","italic":true}]
execute if score #rd dv.tmp matches 4 run title @s actionbar [{"text":"Radio: ","color":"gray"},{"text":"▮▮▮▮ ","color":"dark_red"},{"text":"ESTÁ AQUÍ","color":"dark_red","bold":true}]
execute if score #rd dv.tmp matches 3.. run playsound canon:items.radio_voice player @s ~ ~ ~ 0.7 1
