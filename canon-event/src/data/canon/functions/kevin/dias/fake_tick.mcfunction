function canon:x/links_follow
tag @a remove dv_wtgt
tag @a[gamemode=!spectator,distance=..64,limit=1,sort=nearest] add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players add @s dv.timer 1
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #60 dv.math
execute if score #c dv.tmp matches 1 run playsound canon:kevin.hey hostile @a[distance=..48] ~ ~1.6 ~ 1 0.92
execute if score #c dv.tmp matches 1 run function canon:kevin/dias/fake_call
execute if entity @a[tag=dv_wtgt,distance=..7] run function canon:kevin/dias/fake_reveal
execute if score @s dv.timer matches 800.. run function canon:rig/vanish
tag @a remove dv_wtgt
