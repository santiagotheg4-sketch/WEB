function canon:rig/init_common
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players operation @s dv.mode = #dmode dv.tmp
scoreboard players set @s dv.pmode 1
scoreboard players set @s dv.posecur -1
scoreboard players set @s dv.posereq 0
scoreboard players set @s dv.say -1
scoreboard players set @s dv.idle 200
scoreboard players set @s dv.talkcd 0
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320000
execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320011
attribute @s minecraft:generic.max_health base set 60
data merge entity @s {Health:60f}
attribute @s minecraft:generic.follow_range base set 0
attribute @s minecraft:generic.movement_speed base set 0.2
attribute @s minecraft:generic.attack_damage base set 6
attribute @s minecraft:generic.armor base set 4
attribute @s minecraft:generic.knockback_resistance base set 0.9
attribute @s minecraft:zombie.spawn_reinforcements base set 0
scoreboard players set @s dv.watch 0
scoreboard players set @s dv.lose 0
scoreboard players set @s dv.jeal 0
scoreboard players operation @s dv.timer2 = #visit dv.tmp
summon minecraft:text_display ~ ~2.3 ~ {Tags:["dv_link","dv_dev_bubble","dv_new_link"],billboard:"center",text:'{"text":""}',background:0,see_through:0b,shadow:1b,view_range:0.5f,line_width:170}
execute if score #es dv.tmp matches ..4 run summon minecraft:interaction ~ ~ ~ {Tags:["dv_link","dv_click","dv_dev_click","dv_new_link"],width:0.8f,height:1.95f,response:1b}
execute if score #es dv.tmp matches 5.. run data merge entity @s {Invulnerable:0b}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
execute facing entity @a[tag=dv_tgt,limit=1] feet run tp @s ~ ~ ~ ~ 0
