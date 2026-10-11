function canon:x/seen
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players add @s dv.timer 1
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score #seen dv.tmp matches 0 if score @s dv.watch matches 1.. run scoreboard players remove @s dv.watch 1
execute if score #seen dv.tmp matches 1 if score #m20 dv.clock matches 0 run function canon:alto/stare_fx
execute if score #seen dv.tmp matches 0 if entity @a[tag=dv_wtgt,distance=3..] run function canon:x/creep
scoreboard players set #aint dv.tmp 160
scoreboard players operation #an dv.tmp = #knotes dv.dev
scoreboard players operation #an dv.tmp *= #20 dv.math
scoreboard players operation #aint dv.tmp -= #an dv.tmp
execute if score #seen dv.tmp matches 0 if score @s dv.timer >= #aint dv.tmp run function canon:alto/blink
execute if score @s dv.watch matches 80.. run function canon:alto/lunge
tag @s remove dv_areach
execute if entity @a[tag=dv_wtgt,distance=..4] run tag @s add dv_areach
execute if entity @a[tag=dv_wtgt,distance=..1.8] run function canon:alto/catch
