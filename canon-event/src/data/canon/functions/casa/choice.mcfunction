tag @s add dv_jtalk
scoreboard players operation #jc dv.tmp = @s dv.jr
scoreboard players set @s dv.jr 0
scoreboard players set #jf dv.tmp 0
execute as @e[type=zombie,tag=dv_jcasa,distance=..14,limit=1,sort=nearest] run scoreboard players set #jf dv.tmp 1
execute if score #jf dv.tmp matches 0 run tellraw @s {"text":"Juli no está cerca.","color":"gray","italic":true}
execute if score #jf dv.tmp matches 1 as @e[type=zombie,tag=dv_jcasa,distance=..14,limit=1,sort=nearest] at @s run function canon:casa/c/run
tag @s remove dv_jtalk
