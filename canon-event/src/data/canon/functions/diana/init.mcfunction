function canon:rig/init_common
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players operation @s dv.state = #dstate dv.tmp
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320078
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320087
execute on passengers if entity @s[tag=dv_neck] run scoreboard players set @s dv.cmd 7320093
attribute @s minecraft:generic.follow_range base set 0
attribute @s minecraft:generic.knockback_resistance base set 1
attribute @s minecraft:zombie.spawn_reinforcements base set 0
scoreboard players set @s dv.watch 0
scoreboard players set @s dv.posecur -1
scoreboard players set @s dv.posereq 0
summon minecraft:marker ~ ~1.6 ~ {Tags:["dv_link","dv_dlook","dv_new_link"]}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
scoreboard players operation @e[tag=dv_new_link] dv.target = @s dv.target
tag @e[tag=dv_new_link] remove dv_new_link
execute facing entity @a[tag=dv_dtgt,limit=1] feet run tp @s ~ ~ ~ ~ 0
