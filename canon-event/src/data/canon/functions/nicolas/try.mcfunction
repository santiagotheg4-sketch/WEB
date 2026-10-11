scoreboard players set @s dv.ncd 420
execute if entity @e[type=zombie,tag=dv_nicolas,distance=..96] run scoreboard players set @s dv.ncd 60
execute unless entity @e[type=zombie,tag=dv_nicolas,distance=..96] run function canon:nicolas/try2
