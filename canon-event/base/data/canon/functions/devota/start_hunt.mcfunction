scoreboard players set @s dv.mode 5
scoreboard players set @s dv.timer 0
scoreboard players set @s dv.lose 0
scoreboard players set @s dv.watch 0
data merge entity @s {NoAI:0b,Invulnerable:0b}
attribute @s minecraft:generic.follow_range base set 48
attribute @s minecraft:generic.movement_speed base set 0.33
execute if score #es dv.tmp matches 6 run attribute @s minecraft:generic.movement_speed base set 0.37
function canon:devota/pose/req_normal
function canon:devota/expr/scream
playsound canon:devota.scream hostile @a[distance=..64] ~ ~ ~ 2 1
playsound canon:devota.scream_layer hostile @a[distance=..64] ~ ~ ~ 1.2 1.4
execute if score #susto dv.cfg matches 1 run effect give @a[distance=..40] minecraft:darkness 3 0 true
execute if score #susto dv.cfg matches 1 as @a[distance=..40] run function canon:fx/zoom_in
execute if score #susto dv.cfg matches 1 run playsound canon:fx.stinger master @a[distance=..40] ~ ~ ~ 0.6 1
function canon:luna/react/danger
