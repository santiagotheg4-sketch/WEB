execute if entity @a[tag=dv_tgt,distance=12..,predicate=canon:corriendo] unless score @s dv.talkcd matches 1.. run function canon:devota/runaway
scoreboard players remove @s[scores={dv.talkcd=1..}] dv.talkcd 1
