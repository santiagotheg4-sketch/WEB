tag @s add dv_offering
execute positioned ^ ^1 ^0.8 run loot spawn ~ ~ ~ loot canon:deseos/regalo
playsound canon:fx.gift neutral @a[distance=..16] ~ ~ ~ 0.7 1
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_dev_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"Te traje algo.","color":"#d77a8a"}',background:1342177280}
scoreboard players set @s dv.say 70
playsound canon:ui.blip neutral @a[distance=..16] ~ ~1.6 ~ 0.5 1.25
