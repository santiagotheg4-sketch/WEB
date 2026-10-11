stopsound @a[tag=dv_kpart] record canon:kevin.techno
playsound canon:fx.heartbeat ambient @a[tag=dv_kpart] ~ ~ ~ 1 1
tag @e[type=zombie,tag=dv_fiestero] add dv_fstare
execute as @e[type=block_display,tag=dv_flight] run data merge entity @s {block_state:{Name:"minecraft:red_stained_glass"}}
execute as @e[type=zombie,tag=dv_kevin,limit=1] run tag @s remove dv_kdance
execute as @e[type=zombie,tag=dv_kevin,limit=1] run execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320124
execute as @e[type=zombie,tag=dv_kevin,limit=1] run execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320124
tellraw @a[tag=dv_kpart] {"text":"La música se corta. Todos dejan de bailar. Todos te miran.","color":"#c94a4a","italic":true}
