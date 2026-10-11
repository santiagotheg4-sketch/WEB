scoreboard players set @s dv.car 2
attribute @s minecraft:generic.movement_speed base set 0.34
playsound canon:car.start neutral @a[distance=..48] ~ ~ ~ 1.2 1
playsound canon:car.horn neutral @a[distance=..48] ~ ~ ~ 1 1
title @a[distance=..6] times 10 50 20
title @a[distance=..6] subtitle {"text":"Maneja hacia el norte, pasando la iglesia. No mires atrás.","color":"gray","italic":true}
title @a[distance=..6] title {"text":"¡ARRANCÓ!","color":"#9fd8b0"}
scoreboard players set #townrage dv.dev 1
