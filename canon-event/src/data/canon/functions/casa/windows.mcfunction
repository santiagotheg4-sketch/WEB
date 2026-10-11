scoreboard players add #win dv.dev 1
scoreboard players operation #c dv.tmp = #win dv.dev
scoreboard players operation #c dv.tmp %= #2 dv.math
execute if score #c dv.tmp matches 0 run setblock 4 78 1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=false]
execute if score #c dv.tmp matches 0 run setblock 12 78 1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=false]
execute if score #c dv.tmp matches 1 run setblock 4 78 1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=true]
execute if score #c dv.tmp matches 1 run setblock 12 78 1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=true]
playsound minecraft:block.wooden_trapdoor.open block @a[distance=..40] 8 78 1 0.6 0.8
