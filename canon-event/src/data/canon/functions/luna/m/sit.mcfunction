execute if score #m4 dv.clock matches 0 run function canon:luna/face
execute if entity @a[tag=dv_ltgt,distance=4..] run scoreboard players set @s dv.mode 0
scoreboard players set #still dv.tmp 0
execute if entity @a[tag=dv_ltgt,distance=..6,scores={dv.noise=0}] run scoreboard players set #still dv.tmp 1
execute if score #still dv.tmp matches 1 run scoreboard players add @s dv.idle 1
execute if score #still dv.tmp matches 0 run scoreboard players set @s dv.idle 100
execute if score @s dv.idle matches 700.. run function canon:luna/fall_asleep
