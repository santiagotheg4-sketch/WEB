scoreboard players operation @s dv.mode = @s dv.pmode
scoreboard players set @s dv.timer 0
execute if score @s dv.mode matches 3 run function canon:devota/start_leave
execute if score @s dv.mode matches 0..1 run scoreboard players set @s dv.mode 1
