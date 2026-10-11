scoreboard players set #apagon dv.ev 40
scoreboard players set #apagon_cd dv.ev 520
function canon:town/lamps_off
execute as @a[predicate=canon:en_pueblo] at @s run playsound canon:fx.blackout ambient @s ~ ~ ~ 1 1
execute if score #susto dv.cfg matches 1 run effect give @a[predicate=canon:en_pueblo] minecraft:darkness 3 0 true
title @a[predicate=canon:en_pueblo] actionbar {"text":"Se fue la luz. Ahora te oye mejor.","color":"#c43a4a","italic":true}
