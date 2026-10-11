scoreboard players operation #c2 dv.tmp = @s dv.cmd
scoreboard players operation #c2 dv.tmp += #frame dv.tmp
execute store result entity @s item.tag.CustomModelData int 1 run scoreboard players get #c2 dv.tmp
