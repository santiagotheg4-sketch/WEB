scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=item_display,tag=dv_nota_vis] if score @s dv.id = #id dv.tmp run kill @s
scoreboard players add #knotes dv.dev 1
playsound canon:fx.sub_hit master @a[tag=dv_kpart] ~ ~ ~ 0.8 1
playsound canon:miron.estatica ambient @a[tag=dv_talker] ~ ~ ~ 1 1
function canon:kevin/bosque/nota_text
title @a[tag=dv_kpart] actionbar [{"text":"Notas: ","color":"gray"},{"score":{"name":"#knotes","objective":"dv.dev"},"color":"white"},{"text":"/6","color":"gray"}]
execute if score #knotes dv.dev matches 6.. run function canon:kevin/bosque/win
kill @s
