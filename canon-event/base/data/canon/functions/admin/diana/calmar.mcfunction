scoreboard players set @s dv.dia 0
scoreboard players set @s dv.dcd 300
scoreboard players operation #pid dv.tmp = @s dv.pid
execute as @e[type=zombie,tag=dv_diana] if score @s dv.target = #pid dv.tmp at @s run function canon:diana/despawn
execute if score @s dv.par matches 1.. run function canon:diana/par/release
tellraw @s {"text":"[Canon Event] Diana se calmó.","color":"dark_gray"}
