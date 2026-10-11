tag @s add dv_furn_on_new
tag @e[type=item_display,tag=dv_mueble_tv,distance=..0.6,limit=1,sort=nearest] add dv_tv_on
playsound canon:furniture.tv_static block @a[distance=..16] ~ ~ ~ 0.6 1
tag @s add dv_furn_on
tag @s remove dv_furn_on_new
