scoreboard players add #dr dv.tmp 1
execute positioned ~-0.5 ~-0.9 ~-0.5 if entity @e[type=zombie,tag=dv_dme,dx=0,dy=1,dz=0] run scoreboard players set #dr dv.tmp 1000
execute if score #dr dv.tmp matches ..60 if block ~ ~ ~ #canon:transparente positioned ^ ^ ^0.85 run function canon:diana/look_ray
