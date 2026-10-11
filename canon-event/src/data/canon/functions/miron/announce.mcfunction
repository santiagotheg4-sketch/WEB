scoreboard players set #mironcd dv.dev 420
playsound canon:miron.aparece ambient @s ~ ~ ~ 0.9 0.9
playsound canon:fx.heartbeat ambient @s ~ ~ ~ 0.7 1
execute as @e[type=wolf,tag=dv_luna,distance=..24] at @s run function canon:luna/alarm_watch
