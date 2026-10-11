data modify storage canon:hud p set value []
data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score @s dv.noise matches 0 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score @s dv.noise matches 1 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score @s dv.noise matches 2 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score @s dv.noise matches 3 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score @s dv.noise matches 4 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score @s dv.noise matches 5 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
scoreboard players operation #hs dv.tmp = #stage dv.dev
execute if predicate canon:en_pueblo if score #townmode dv.dev matches 1 if score #hs dv.tmp matches ..4 run scoreboard players set #hs dv.tmp 5
execute if score #hs dv.tmp matches 0 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hs dv.tmp matches 1 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hs dv.tmp matches 2 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hs dv.tmp matches 3 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hs dv.tmp matches 4 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hs dv.tmp matches 5 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hs dv.tmp matches 6 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
scoreboard players operation #hk dv.tmp = #sane dv.dev
scoreboard players operation #hk dv.tmp /= #100 dv.math
execute if score #hs dv.tmp matches 0 run scoreboard players set #hk dv.tmp 10
execute if score #hk dv.tmp matches 0 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 1 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 2 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 3 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 4 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 5 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 6 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 7 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 8 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 9 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #hk dv.tmp matches 10 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
scoreboard players set #ha dv.tmp 0
execute if score @s dv.seen matches 1.. run scoreboard players add #ha dv.tmp 10
execute if score #lalert dv.dev matches 1.. run scoreboard players add #ha dv.tmp 1
execute if score #lalert dv.dev matches 1.. if score #m20 dv.clock matches 10.. run scoreboard players add #ha dv.tmp 1
execute if score #ha dv.tmp matches 0 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #ha dv.tmp matches 1 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #ha dv.tmp matches 2 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #ha dv.tmp matches 10 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #ha dv.tmp matches 11 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
execute if score #ha dv.tmp matches 12 run data modify storage canon:hud p append value '{"text":"","font":"canon:hud2","color":"white"}'
title @s actionbar {"nbt":"p[]","storage":"canon:hud","interpret":true,"separator":""}
