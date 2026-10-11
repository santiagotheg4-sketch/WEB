playsound canon:kevin.laugh neutral @a[distance=..20] ~ ~1.6 ~ 1 1
tag @s add dv_klaugh
scoreboard players set @s dv.timer2 40
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320123
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320123
