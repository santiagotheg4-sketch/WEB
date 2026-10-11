execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.085 run tp @s ~ ~ ~ ~ ~
scoreboard players add @s dv.timer 1
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #40 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:masa.arrastre hostile @a[distance=..24] ~ ~ ~ 1 1
execute if score #c dv.tmp matches 0 run particle minecraft:block minecraft:redstone_block ~ ~0.3 ~ 0.6 0.2 0.6 0 12 normal
scoreboard players remove @s[scores={dv.timer2=1..}] dv.timer2 1
execute if entity @a[tag=dv_wtgt,distance=..1.8] unless score @s dv.timer2 matches 1.. run function canon:masa/hit
