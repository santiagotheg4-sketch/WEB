scoreboard players set @s dv.timer2 -1
tag @s remove dv_klaugh
tag @s remove dv_koffer
execute unless score @s dv.mode matches 1 run tag @s remove dv_kdance
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320122
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320122
