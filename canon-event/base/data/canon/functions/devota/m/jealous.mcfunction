execute if score @s dv.timer matches 1 run function canon:devota/expr/scream
execute if score @s dv.timer matches 1 run playsound canon:devota.scream hostile @a[distance=..32] ~ ~ ~ 1 1.3
execute if score @s dv.timer matches 2 at @a[tag=dv_tgt,limit=1] as @e[type=#canon:celos,distance=..8,limit=1,sort=nearest] at @s run function canon:devota/jealous_hit
execute if score @s dv.timer matches 2 run function canon:luna/react/jealous
execute if score @s dv.timer matches 4 run function canon:devota/expr/grin
execute if score @s dv.timer matches 4 run scoreboard players remove #sane dv.dev 10
execute if score @s dv.timer matches 4 run function canon:devota/jealous_say
execute if score @s dv.timer matches 30 run scoreboard players operation @s dv.mode = @s dv.pmode
