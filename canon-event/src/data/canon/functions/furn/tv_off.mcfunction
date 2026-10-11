tag @s remove dv_furn_on
execute as @e[type=item_display,tag=dv_mueble_tv,distance=..0.6,limit=1,sort=nearest] run function canon:furn/tv_dark
playsound minecraft:block.lever.click block @a[distance=..16] ~ ~ ~ 0.6 0.6
