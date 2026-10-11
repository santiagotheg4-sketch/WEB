execute store result score #py dv.tmp run data get entity @s Pos[1] 1000
scoreboard players operation #vy dv.tmp = #py dv.tmp
execute on vehicle store result score #vy dv.tmp run data get entity @s Pos[1] 1000
scoreboard players operation #py dv.tmp -= #vy dv.tmp
scoreboard players operation @s dv.calib = #py dv.tmp
execute store result score #ty dv.tmp run data get entity @s transformation.translation[1] 1000
scoreboard players operation #ty dv.tmp -= #py dv.tmp
execute store result entity @s transformation.translation[1] float 0.001 run scoreboard players get #ty dv.tmp
execute if score #flip dv.cfg matches 1 run data modify entity @s transformation.right_rotation set value [0f,1f,0f,0f]
execute store result entity @s item.tag.CustomModelData int 1 run scoreboard players get @s dv.cmd
tag @s remove dv_cal3
tag @s add dv_ready
execute on vehicle run scoreboard players set @s dv.frame -1
