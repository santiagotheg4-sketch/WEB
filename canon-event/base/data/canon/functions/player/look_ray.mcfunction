scoreboard players add #r dv.tmp 1
execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[type=zombie,tag=dv_devota,dx=0,dy=0,dz=0] run scoreboard players set #r dv.tmp 1000
execute if score #r dv.tmp matches 1000 run scoreboard players set @a[tag=dv_looker,limit=1] dv.seen 1
execute if score #r dv.tmp matches ..70 if block ~ ~ ~ #canon:transparente positioned ^ ^ ^0.5 run function canon:player/look_ray
