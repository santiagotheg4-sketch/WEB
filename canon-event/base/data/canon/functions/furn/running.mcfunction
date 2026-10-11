scoreboard players remove @s[scores={dv.timer=1..}] dv.timer 1
execute if entity @s[tag=dv_furn_rocola] if score @s dv.timer matches ..0 run function canon:furn/rocola_play
execute if entity @s[tag=dv_furn_radio_antigua] if score @s dv.timer matches ..0 run function canon:furn/radio_play
execute if entity @s[tag=dv_furn_tv] if predicate canon:azar/1en10 run playsound canon:furniture.tv_static block @a[distance=..12] ~ ~ ~ 0.3 1
