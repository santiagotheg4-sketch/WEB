scoreboard players operation #a dv.tmp = @s dv.resp
scoreboard players set @s dv.resp 0
execute if score #qt dv.dev matches 1.. if score #a dv.tmp = #qgood dv.dev as @e[type=zombie,tag=dv_devota,limit=1] at @s run function canon:devota/q/good
execute if score #qt dv.dev matches 1.. unless score #a dv.tmp = #qgood dv.dev as @e[type=zombie,tag=dv_devota,limit=1] at @s run function canon:devota/q/bad
scoreboard players set #qt dv.dev 0
