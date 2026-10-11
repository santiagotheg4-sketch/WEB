tag @a remove dv_focus
execute if score #townmode dv.dev matches 1 as @r[predicate=canon:en_pueblo] run tag @s add dv_focus
execute unless score #townmode dv.dev matches 1 as @r[predicate=canon:en_superficie,predicate=!canon:espectador] run tag @s add dv_focus
execute if entity @a[tag=dv_focus] run function canon:devota/g/roll
tag @a remove dv_focus
