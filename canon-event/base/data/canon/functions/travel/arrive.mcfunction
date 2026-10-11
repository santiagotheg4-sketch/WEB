scoreboard players set @s dv.travel 0
execute in canon:valle_quieto run tp @s 7.5 64 -109.5 0 0
effect clear @s minecraft:blindness
effect clear @s minecraft:slowness
effect clear @s minecraft:resistance
effect give @s minecraft:darkness 3 0 true
playsound canon:fx.bus ambient @s ~ ~ ~ 0.6 0.8
title @s times 20 70 30
title @s subtitle {"text":"Población: 1.311... ahora 1.312","color":"gray","italic":true}
title @s title {"text":"VALLE QUIETO","color":"#c9c9c9"}
