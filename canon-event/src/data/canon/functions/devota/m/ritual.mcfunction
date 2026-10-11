execute if score @s dv.timer matches 1 run function canon:devota/face
execute if score @s dv.timer matches 1 run function canon:devota/expr/stare
execute if score @s dv.timer matches 4 run function canon:devota/pose/req_tilt90
execute if score @s dv.timer matches 40 run playsound canon:diana.crack hostile @a[distance=..24] ~ ~1.6 ~ 0.8 1.3
execute if score @s dv.timer matches 40..60 if score #m4 dv.clock matches 0 run function canon:devota/body/twitch_l
execute if score @s dv.timer matches 40..60 if score #m4 dv.clock matches 2 run function canon:devota/body/twitch_r
execute if score @s dv.timer matches 61 run function canon:devota/body/straight
execute if score @s dv.timer matches 62 run function canon:devota/pose/req_snap
execute if score @s dv.timer matches 62 run function canon:devota/expr/grin
execute if score @s dv.timer matches 62 run playsound canon:devota.giggle hostile @a[distance=..24] ~ ~ ~ 0.8 1.2
execute if score @s dv.timer matches 66 run tag @s add dv_fastwave
execute if score @s dv.timer matches 66 run playsound canon:devota.hum hostile @a[distance=..24] ~ ~ ~ 0.6 1.4
execute if score @s dv.timer matches 112 run tag @s remove dv_fastwave
execute if score @s dv.timer matches 112 run function canon:devota/pose/req_back
execute if score @s dv.timer matches 142 run function canon:devota/pose/req_normal
execute if score @s dv.timer matches 168 run function canon:devota/expr/love
execute if score @s dv.timer matches 168 run function canon:devota/talk_line
execute if score @s dv.timer matches 185.. run function canon:devota/ritual_end
