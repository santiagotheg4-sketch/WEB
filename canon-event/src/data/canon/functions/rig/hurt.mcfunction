tag @s add dv_hurt
tag @s add dv_flashing
scoreboard players set @s dv.flash 4
execute on passengers if entity @s[tag=dv_ready] run data merge entity @s {Glowing:1b,glow_color_override:12582912}
particle minecraft:damage_indicator ~ ~1 ~ 0.2 0.3 0.2 0.1 3 normal
