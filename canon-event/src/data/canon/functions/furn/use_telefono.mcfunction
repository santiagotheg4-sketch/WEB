execute if entity @s[tag=dv_ringing] run function canon:furn/phone_answer
execute unless entity @s[tag=dv_ringing] run playsound minecraft:block.note_block.bit block @a[distance=..8] ~ ~ ~ 0.5 0.5
