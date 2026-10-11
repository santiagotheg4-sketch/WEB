setblock ~ ~1 ~ minecraft:air
execute as @e[type=item_display,tag=dv_mueble_lampara,distance=..0.6,limit=1,sort=nearest] run data merge entity @s {brightness:{sky:0,block:0}}
playsound minecraft:block.lever.click block @a[distance=..16] ~ ~ ~ 0.5 0.6
