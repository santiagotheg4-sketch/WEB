function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320142
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320142
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.watch 0
