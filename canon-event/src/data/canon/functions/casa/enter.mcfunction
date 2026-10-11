function canon:travel/store_return
scoreboard players set @s dv.sb 6000
scoreboard players set @s dv.mus 0
scoreboard players set @s dv.kz 0
execute in canon:sueno_blanco run tp @s 12.5 64 -12.5 0 5
effect give @s minecraft:blindness 2 0 true
title @s times 20 70 30
title @s subtitle {"text": "Todo es blanco. Menos la casa.", "color": "#cfcfcf", "italic": true}
title @s title {"text": "LA CASA", "color": "#ffffff"}
playsound canon:fx.whoosh_white master @s ~ ~ ~ 1 1
execute if score #casa_built dv.build matches 0 run function canon:casa/build_start
tellraw @s {"text": "(Estás soñando. Juli está en algún lugar de la casa. Si te alejas mucho, despiertas.)", "color": "gray", "italic": true}
