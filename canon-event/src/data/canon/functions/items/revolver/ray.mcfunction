scoreboard players add #ray dv.tmp 1
execute if score #ray dv.tmp matches 4.. run particle minecraft:crit ~ ~ ~ 0 0 0 0 1 normal
execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[type=!#canon:no_disparable,tag=!dv_shooter,dx=0,dy=0,dz=0,limit=1,sort=nearest] run function canon:items/revolver/hit
execute if score #ray dv.tmp matches ..80 unless block ~ ~ ~ #canon:atravesable run function canon:items/revolver/wall
execute if score #ray dv.tmp matches ..80 if block ~ ~ ~ #canon:atravesable positioned ^ ^ ^0.5 run function canon:items/revolver/ray
