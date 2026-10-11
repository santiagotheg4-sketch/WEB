execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
scoreboard players set #bok dv.tmp 0
execute if entity @a[tag=dv_ktalk,predicate=canon:de_noche,predicate=canon:en_bosque] run scoreboard players set #bok dv.tmp 1
execute unless score #kev dv.dev matches 1.. if score #bok dv.tmp matches 0 run function canon:kevin/bosque/no
execute unless score #kev dv.dev matches 1.. if score #bok dv.tmp matches 1 at @a[tag=dv_ktalk,limit=1] run function canon:kevin/bosque/start
