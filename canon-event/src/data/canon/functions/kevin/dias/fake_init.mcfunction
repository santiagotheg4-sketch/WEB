function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320115
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320115
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320122
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320122
function canon:x/add_bubble
