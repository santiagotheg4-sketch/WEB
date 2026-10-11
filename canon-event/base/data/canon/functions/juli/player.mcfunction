execute if entity @s[name=tantanto4] run tag @s add dv_santi
scoreboard players add @s dv.juli 1
execute if predicate canon:en_banca_juli run scoreboard players add @s dv.juli 3
scoreboard players remove @s[scores={dv.jcd=1..}] dv.jcd 1
scoreboard players set #busy dv.tmp 0
execute if score @s dv.par matches 1.. run scoreboard players set #busy dv.tmp 1
execute if score @s dv.escena matches 1.. run scoreboard players set #busy dv.tmp 1
execute if entity @e[type=zombie,tag=dv_juli,distance=..80] run scoreboard players set #busy dv.tmp 1
scoreboard players operation #pid dv.tmp = @s dv.pid
execute as @e[type=zombie,tag=dv_diana,distance=..80] if score @s dv.target = #pid dv.tmp run scoreboard players set #busy dv.tmp 1
execute if score #busy dv.tmp matches 0 if entity @s[tag=dv_santi] if score @s dv.juli matches 480.. run function canon:juli/try_search
execute if score #busy dv.tmp matches 0 unless entity @s[tag=dv_santi] if score @s dv.juli matches 300.. if score @s dv.jcd matches ..0 run function canon:juli/try_ask
