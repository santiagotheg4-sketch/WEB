scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches ..0 if entity @a[distance=..5] run function canon:vago/say
