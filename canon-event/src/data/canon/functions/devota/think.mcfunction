scoreboard players add @s dv.timer 1
scoreboard players remove @s[scores={dv.timer2=1..}] dv.timer2 1
execute unless score @s dv.posereq = @s dv.posecur run function canon:devota/pose/sync
execute at @a[tag=dv_tgt,limit=1] run function canon:devota/g/es
function canon:devota/senses
tag @s remove dv_walking
execute if score @s dv.mode matches 0 run function canon:devota/m/arrive
execute if score @s dv.mode matches 1 run function canon:devota/m/follow
execute if score @s dv.mode matches 2 run function canon:devota/m/watch
execute if score @s dv.mode matches 3 run function canon:devota/m/leave
execute if score @s dv.mode matches 4 run function canon:devota/m/stalk
execute if score @s dv.mode matches 5 run function canon:devota/m/hunt
execute if score @s dv.mode matches 6 run function canon:devota/m/search
execute if score @s dv.mode matches 7 run function canon:devota/m/ritual
execute if score @s dv.mode matches 8 run function canon:devota/m/jealous
execute if entity @s[tag=dv_hurt] run function canon:devota/hurt_react
tag @s remove dv_hurt
execute if score #m40 dv.clock matches 0 if score #d dv.tmp matches ..16 if score #es dv.tmp matches 4.. run playsound canon:fx.heartbeat ambient @a[distance=..16] ~ ~ ~ 0.6 1
execute if score #m20 dv.clock matches 10 if score #d dv.tmp matches ..8 if score #es dv.tmp matches 5.. run playsound canon:fx.heartbeat_fast ambient @a[distance=..8] ~ ~ ~ 0.8 1
