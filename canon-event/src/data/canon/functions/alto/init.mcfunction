function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320144
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320144
scoreboard players set @s dv.watch 0
playsound canon:alto.aparece hostile @a[tag=dv_kpart] ~ ~ ~ 0.6 0.8
