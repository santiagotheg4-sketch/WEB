scoreboard players set @s dv.death 0
scoreboard players set @s dv.inv 0
scoreboard players set @s dv.pill 0
scoreboard players set @s dv.sleep 0
scoreboard players set @s dv.rain 0
execute if score @s dv.par matches 1.. run function canon:diana/par/release
scoreboard players set @s dv.escena 0
scoreboard players set @s dv.sueno 0
scoreboard players set @s dv.sfase 0
scoreboard players set @s dv.lint 0
function canon:devota/g/player_died
execute if score @s dv.town matches 1 run function canon:town/died_here
