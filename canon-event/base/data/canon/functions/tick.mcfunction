scoreboard players add #t dv.clock 1
scoreboard players operation #m2 dv.clock = #t dv.clock
scoreboard players operation #m2 dv.clock %= #2 dv.math
scoreboard players operation #m4 dv.clock = #t dv.clock
scoreboard players operation #m4 dv.clock %= #4 dv.math
scoreboard players operation #m10 dv.clock = #t dv.clock
scoreboard players operation #m10 dv.clock %= #10 dv.math
scoreboard players operation #m20 dv.clock = #t dv.clock
scoreboard players operation #m20 dv.clock %= #20 dv.math
scoreboard players operation #m40 dv.clock = #t dv.clock
scoreboard players operation #m40 dv.clock %= #40 dv.math
scoreboard players operation #m200 dv.clock = #t dv.clock
scoreboard players operation #m200 dv.clock %= #200 dv.math
execute as @e[type=item_display,tag=dv_cal3] at @s run function canon:rig/calibrate
execute as @a at @s run function canon:player/tick
tag @e[tag=dv_act] remove dv_act
execute as @a at @s run tag @e[tag=dv_brain,distance=..96] add dv_act
execute as @e[type=zombie,tag=dv_devota] at @s run function canon:devota/tick
execute as @e[type=zombie,tag=dv_mariana,tag=dv_act] at @s run function canon:mariana/tick
execute as @e[type=cave_spider,tag=dv_gato,tag=dv_act] at @s run function canon:gato/tick
execute as @e[type=chicken,tag=dv_cuervo,tag=dv_act] at @s run function canon:cuervo/tick
execute as @e[type=endermite,tag=dv_rata,tag=dv_act] at @s run function canon:rata/tick
execute as @e[type=wandering_trader,tag=dv_vago,tag=dv_act] at @s run function canon:vago/tick
execute as @e[type=wandering_trader,tag=dv_tendero,tag=dv_act] at @s run function canon:tendero/tick
execute as @e[type=horse,tag=dv_car] at @s run function canon:car/tick
execute as @e[type=zombie,tag=dv_diana] at @s run function canon:diana/tick
execute as @e[type=zombie,tag=dv_juli] at @s run function canon:juli/tick
execute as @e[type=wolf,tag=dv_luna] at @s run function canon:luna/tick
execute as @e[tag=dv_npc2] at @s run function canon:npc2/tick
execute as @e[tag=dv_act,tag=!dv_car] at @s run function canon:rig/visual
execute as @a at @s as @e[type=interaction,tag=dv_click,distance=..7] run function canon:click/poll
execute if score #built dv.build matches 1 run function canon:town/build/tick
execute if score #built dv.build matches 2 if entity @a[predicate=canon:en_pueblo] run function canon:escape/fast
execute if score #m4 dv.clock matches 0 as @a at @s as @e[type=item_display,tag=dv_tv_on,distance=..20] at @s run function canon:furn/tv_frame
execute as @e[type=item_frame,tag=dv_place] at @s run function canon:furn/place
execute if score #m10 dv.clock matches 0 run function canon:rig/cleanup
execute if score #m20 dv.clock matches 0 run function canon:slow_tick
function canon:rig/cal_shift
