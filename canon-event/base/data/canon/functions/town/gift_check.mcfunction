execute if entity @s[nbt={Health:0.0f}] run scoreboard players set #dead dv.tmp 1
execute unless entity @s[nbt={Health:0.0f}] run function canon:town/gift_give
