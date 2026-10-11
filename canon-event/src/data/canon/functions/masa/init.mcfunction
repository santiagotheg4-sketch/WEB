function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320148
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320148
playsound canon:masa.rugido hostile @a[distance=..48] ~ ~ ~ 1 0.7
