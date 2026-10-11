scoreboard players set #ly dv.tmp 1723
execute if score @s dv.posecur matches 4 run scoreboard players set #ly dv.tmp 2323
execute if score @s dv.posecur matches 5 run scoreboard players set #ly dv.tmp 2723
execute if score @s dv.posecur matches 1 run scoreboard players set #ly dv.tmp 568
execute as @e[type=marker,tag=dv_dlook] if score @s dv.id = #id dv.tmp run function canon:diana/look_marker_move
