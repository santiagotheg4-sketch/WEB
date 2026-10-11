scoreboard players set @s dv.timer2 24
damage @a[tag=dv_wtgt,limit=1] 3 minecraft:mob_attack by @s
playsound canon:nicolas.risa hostile @a[distance=..16] ~ ~ ~ 1 1.1
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320132
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320132
