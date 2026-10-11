scoreboard players set #townmode dv.dev 1
scoreboard players set #tcalm dv.dev -1
scoreboard players set #cd dv.dev 0
execute unless score #met dv.dev matches 1 run function canon:devota/g/met
execute as @e[type=zombie,tag=dv_devota] at @s run function canon:rig/despawn
execute in canon:valle_quieto run function canon:town/apagon_start
title @a[predicate=canon:en_pueblo] times 5 60 25
title @a[predicate=canon:en_pueblo] subtitle {"text":"Alguien en Valle Quieto te reconoció.","color":"#d77a8a","italic":true}
title @a[predicate=canon:en_pueblo] title {"text":"EL PUEBLO DESPERTÓ","color":"#c43a4a","bold":true}
execute as @a[predicate=canon:en_pueblo] at @s run playsound canon:devota.scream master @s ~ ~ ~ 0.7 0.9
execute as @a[predicate=canon:en_pueblo] run function canon:fx/shake_big
