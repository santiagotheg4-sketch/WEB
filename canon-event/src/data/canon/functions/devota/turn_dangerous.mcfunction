scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=interaction,tag=dv_dev_click] if score @s dv.id = #id dv.tmp run kill @s
data merge entity @s {Invulnerable:0b}
function canon:devota/clear_acts
execute unless score @s dv.mode matches 4..6 run function canon:devota/to_stalk
