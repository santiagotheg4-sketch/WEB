scoreboard players set @s dv.sb 0
stopsound @s music canon:music.casa_blanca
title @s times 0 10 40
title @s subtitle ""
title @s title ["",{"text":"\ue104","font":"canon:susto","color":"white"}]
function canon:util/tp_return
playsound canon:fx.wake_gasp player @s ~ ~ ~ 1 1
tellraw @s {"text": "Despiertas. Soñaste con una casa de madera y con Juli. No recuerdas qué te dijo.", "color": "#f2a7c3", "italic": true}
