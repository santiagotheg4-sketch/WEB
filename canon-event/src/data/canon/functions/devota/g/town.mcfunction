execute unless entity @a[predicate=canon:en_pueblo] run function canon:devota/g/town_empty
execute if entity @a[predicate=canon:en_pueblo] if score #tcalm dv.dev matches 1.. run scoreboard players remove #tcalm dv.dev 1
execute if entity @a[predicate=canon:en_pueblo] if score #tcalm dv.dev matches 0 unless score #townmode dv.dev matches 1 run function canon:devota/g/town_turn
