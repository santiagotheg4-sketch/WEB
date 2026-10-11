execute if block ~ ~1 ~ minecraft:air run setblock ~ ~1 ~ minecraft:light[level=13,waterlogged=false]
execute as @e[type=item_display,tag=dv_mueble_lampara,distance=..0.6,limit=1,sort=nearest] run data merge entity @s {brightness:{sky:0,block:13}}
playsound minecraft:block.lever.click block @a[distance=..16] ~ ~ ~ 0.5 1.0
