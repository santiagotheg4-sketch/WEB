scoreboard players set @s dv.sueno 0
scoreboard players set @s dv.sfase 0
title @s times 0 10 40
title @s subtitle ""
title @s title ["",{"text":"","font":"canon:susto","color":"white"}]
stopsound @s music canon:music.el_sueno
function canon:util/tp_return
playsound canon:fx.wake_gasp player @s ~ ~ ~ 1 1
effect give @s minecraft:slow_falling 4 0 true
execute unless score @s dv.jline matches 100.. run function canon:sueno/first_wake
tellraw @s {"text":"Despiertas. Todavía hueles a flores.","color":"#f2a7c3","italic":true}
