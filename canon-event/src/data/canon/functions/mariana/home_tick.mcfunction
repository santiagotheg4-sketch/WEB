scoreboard players remove @s[scores={dv.timer=1..}] dv.timer 1
execute if score @s dv.timer matches ..0 if entity @a[distance=..40] unless entity @e[type=zombie,tag=dv_mariana,distance=..80] run function canon:spawn/mariana
