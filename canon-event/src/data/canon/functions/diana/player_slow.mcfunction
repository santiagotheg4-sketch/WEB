scoreboard players set #inc dv.tmp 0
execute if predicate canon:de_noche if predicate canon:azar/50 run scoreboard players add #inc dv.tmp 1
execute if predicate canon:oscuro if predicate canon:azar/50 run scoreboard players add #inc dv.tmp 1
execute if entity @s[y=-64,dy=110] unless predicate canon:iluminado if predicate canon:azar/1en3 run scoreboard players add #inc dv.tmp 1
execute if predicate canon:en_casa_diana run scoreboard players add #inc dv.tmp 5
execute if predicate canon:de_dia if predicate canon:iluminado if predicate canon:azar/50 run scoreboard players remove #inc dv.tmp 1
execute if score @s dv.par matches 1.. run scoreboard players set #inc dv.tmp 0
scoreboard players operation @s dv.dia += #inc dv.tmp
scoreboard players set @s[scores={dv.dia=..-1}] dv.dia 0
scoreboard players set @s[scores={dv.dia=1001..}] dv.dia 1000
scoreboard players remove @s[scores={dv.dcd=1..}] dv.dcd 1
scoreboard players remove @s[scores={dv.dhunt=1..}] dv.dhunt 1
scoreboard players remove @s[scores={dv.parcd=1..}] dv.parcd 20
scoreboard players remove @s[scores={dv.dleft=1..}] dv.dleft 1
execute if score @s dv.dleft matches 1 run tellraw @s {"translate":"multiplayer.player.left","with":["Diana la Zunga"],"color":"yellow"}
execute if predicate canon:en_casa_diana unless entity @s[tag=dv_en_casa] run function canon:diana/casa_enter
execute unless predicate canon:en_casa_diana run tag @s remove dv_en_casa
execute if predicate canon:en_altar_diana run function canon:diana/altar_tick
execute if score @s dv.dia matches 100.. if score @s dv.dcd matches ..0 unless score @s dv.par matches 1.. unless score @s dv.escena matches 1.. unless predicate canon:espectador run function canon:diana/event_roll
execute if score @s dv.bat matches ..1200 if score @s dv.bat matches -999999..999999 run function canon:items/linterna/recharge
