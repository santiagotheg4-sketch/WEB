effect give @s minecraft:invisibility infinite 0 true
attribute @s minecraft:generic.movement_speed base set 0
attribute @s minecraft:horse.jump_strength base set 0
attribute @s minecraft:generic.max_health base set 100
data merge entity @s {Health:100f}
scoreboard players operation @s dv.id = #next dv.id
scoreboard players operation @e[type=item_display,tag=dv_carbody_new,distance=..1] dv.id = #next dv.id
scoreboard players add #next dv.id 1
scoreboard players set @e[type=item_display,tag=dv_carbody_new,distance=..1] dv.cmd 7320065
execute as @e[type=item_display,tag=dv_carbody_new,distance=..1] run data modify entity @s item.tag.CustomModelData set value 7320065
tag @e[type=item_display,tag=dv_carbody_new,distance=..1] add dv_ready
tag @e[type=item_display,tag=dv_carbody_new,distance=..1] remove dv_carbody_new
scoreboard players set @s dv.calib 0
tag @s remove dv_car_new
