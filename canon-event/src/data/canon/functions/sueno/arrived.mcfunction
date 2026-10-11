scoreboard players set @s dv.sfase 0
tp @s 0.5 153.0 4.5 180 0
effect give @s minecraft:slow_falling 4 0 true
title @s times 10 70 30
title @s subtitle {"text":"Aquí siempre está a punto de amanecer.","color":"#f2a7c3","italic":true}
title @s title {"text":"EL SUEÑO","color":"#ffe3ee"}
playsound canon:juli.chime ambient @s ~ ~ ~ 0.8 1
playsound canon:music.el_sueno music @s ~ ~ ~ 0.8 1
scoreboard players set #found dv.tmp 0
execute in canon:el_sueno if entity @e[type=zombie,tag=dv_juli,x=2.5,y=153.0,z=-1.5,distance=..64] run scoreboard players set #found dv.tmp 1
execute if score #found dv.tmp matches 0 in canon:el_sueno positioned 2.5 153.0 -1.5 run function canon:sueno/spawn_juli
