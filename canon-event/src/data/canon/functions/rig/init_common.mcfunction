effect give @s minecraft:invisibility infinite 0 true
scoreboard players operation @s dv.id = #next dv.id
execute on passengers run scoreboard players operation @s dv.id = #next dv.id
scoreboard players add #next dv.id 1
scoreboard players set @s dv.frame -1
scoreboard players set @s dv.anim 0
scoreboard players set @s dv.state 0
scoreboard players set @s dv.timer 0
scoreboard players set @s dv.timer2 0
scoreboard players set @s dv.flash 0
execute store result score @s dv.hp run data get entity @s Health 10
scoreboard players operation @s dv.hpold = @s dv.hp
tag @s remove dv_new
