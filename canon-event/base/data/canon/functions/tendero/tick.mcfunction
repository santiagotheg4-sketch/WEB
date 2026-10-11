scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches ..0 if entity @s[tag=dv_vidente] if entity @a[distance=..5] run function canon:tendero/say_vidente
execute if score @s dv.say matches ..0 if entity @s[tag=dv_farmaceuta] if entity @a[distance=..5] run function canon:tendero/say_farmaceuta
execute if score @s dv.say matches ..0 if entity @s[tag=dv_empenista] if entity @a[distance=..5] run function canon:tendero/say_empenista
execute if score #m4 dv.clock matches 0 if entity @a[distance=..6] facing entity @p feet run tp @s ~ ~ ~ ~ ~
