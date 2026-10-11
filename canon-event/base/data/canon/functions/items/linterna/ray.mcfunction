scoreboard players add #lr dv.tmp 1
execute positioned ~-0.6 ~-1.0 ~-0.6 as @e[type=zombie,tag=dv_diana,dx=0.2,dy=1,dz=0.2,limit=1] at @s run function canon:diana/lit_up
execute if score #lr dv.tmp matches ..24 if block ~ ~ ~ #canon:transparente positioned ^ ^ ^1 run function canon:items/linterna/ray
