function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320126
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320126
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320130
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320130
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.say -1
scoreboard players set @s dv.timer2 60
function canon:x/add_bubble
