tag @s add dv_ktalk
scoreboard players set #kc dv.tmp 0
scoreboard players operation #kc dv.tmp = @s dv.kv
scoreboard players set @s dv.kv 0
scoreboard players set #kfound dv.tmp 0
execute as @e[type=zombie,tag=dv_kevin,distance=..16,limit=1,sort=nearest] run scoreboard players set #kfound dv.tmp 1
execute if score #kc dv.tmp matches 21..22 run function canon:kevin/fiesta/drink_choice
execute if score #kfound dv.tmp matches 0 unless score #kc dv.tmp matches 21..22 run tellraw @s {"text":"Kevin no está cerca.","color":"gray","italic":true}
execute if score #kfound dv.tmp matches 1 unless score #kc dv.tmp matches 21..22 as @e[type=zombie,tag=dv_kevin,distance=..16,limit=1,sort=nearest] at @s run function canon:kevin/c/run
tag @s remove dv_ktalk
