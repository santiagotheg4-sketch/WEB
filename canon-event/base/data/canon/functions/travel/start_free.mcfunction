execute unless predicate canon:en_pueblo run function canon:travel/store_return
scoreboard players set @s dv.travel 1
effect give @s minecraft:blindness infinite 0 true
effect give @s minecraft:slowness infinite 6 true
effect give @s minecraft:resistance infinite 4 true
playsound canon:fx.bus ambient @s ~ ~ ~ 1 1
title @s times 20 80 20
title @s subtitle {"text":"El autobús avanza entre la niebla...","color":"gray","italic":true}
title @s title {"text":" "}
execute if score #built dv.build matches 0 run function canon:town/build/start
