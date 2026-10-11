function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320139
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320139
scoreboard players set @s dv.anim 6
execute facing entity @e[type=marker,tag=dv_fiesta_c,limit=1] feet run tp @s ~ ~ ~ ~ 0
