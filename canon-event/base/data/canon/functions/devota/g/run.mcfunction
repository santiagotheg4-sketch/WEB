execute if score #met dv.dev matches 1 run scoreboard players add #decay dv.dev 1
execute if score #decay dv.dev matches 20.. run function canon:devota/g/decay
function canon:devota/g/clamp
function canon:devota/g/stage
execute if score #cd dv.dev matches 1.. run scoreboard players remove #cd dv.dev 1
execute if score #qt dv.dev matches 1.. run function canon:devota/q/tick
scoreboard players set #present dv.dev 0
execute if entity @e[type=zombie,tag=dv_devota] run scoreboard players set #present dv.dev 1
function canon:devota/g/town
execute if score #present dv.dev matches 0 if score #cd dv.dev matches ..0 run function canon:devota/g/try_visit
scoreboard players set @a dv.obs 0
execute if score #stage dv.dev matches 5.. run scoreboard players operation @a dv.obs = #love dv.dev
execute if score #townmode dv.dev matches 1 run scoreboard players set @a[predicate=canon:en_pueblo,scores={dv.obs=..0}] dv.obs 1
