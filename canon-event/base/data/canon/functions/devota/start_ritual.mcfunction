scoreboard players operation @s dv.pmode = @s dv.mode
execute if score @s dv.pmode matches 7 run scoreboard players set @s dv.pmode 3
scoreboard players set @s dv.mode 7
scoreboard players set @s dv.timer 0
function canon:devota/clear_acts
