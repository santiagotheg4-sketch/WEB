playsound minecraft:entity.minecart.riding block @a[distance=..12] ~ ~ ~ 0.4 0.6
execute as @e[type=item_display,tag=dv_mueble_lavadora,distance=..0.6,limit=1,sort=nearest] run function canon:furn/shake
