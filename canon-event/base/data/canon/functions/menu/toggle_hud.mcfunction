execute if score @s dv.hud matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score @s dv.hud matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation @s dv.hud = #tg dv.tmp
execute if score @s dv.hud matches 1 run tellraw @s {"text":"HUD de ruido: activado.","color":"#9fd8b0"}
execute if score @s dv.hud matches 0 run tellraw @s {"text":"HUD de ruido: oculto.","color":"gray"}
