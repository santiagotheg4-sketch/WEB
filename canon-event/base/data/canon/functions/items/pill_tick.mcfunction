scoreboard players remove @s dv.pill 1
execute if score @s dv.pill matches 40 run playsound canon:fx.heartbeat ambient @s ~ ~ ~ 1 0.6
execute if score @s dv.pill matches 0 run damage @s 1000 canon:pastillas
