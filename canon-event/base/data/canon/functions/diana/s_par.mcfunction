execute if score @s dv.timer matches 1 run function canon:diana/pose/req_tilt
execute if score @s dv.timer matches 1..90 run function canon:diana/face
execute if score @s dv.timer matches 50 run playsound canon:diana.crack hostile @a[tag=dv_dtgt] ~ ~1 ~ 1 0.9
execute if score @s dv.timer matches 50 run tag @s add dv_djitter
execute if score @s dv.timer matches 50 run function canon:diana/expr/twisted
execute if score @s dv.timer matches 50..88 if score #m4 dv.clock matches 0 run function canon:diana/body/roll_l
execute if score @s dv.timer matches 50..88 if score #m4 dv.clock matches 2 run function canon:diana/body/roll_r
execute if score @s dv.timer matches 90 run function canon:diana/body/straight
execute if score @s dv.timer matches 90 run tag @s remove dv_djitter
execute if score @s dv.timer matches 92 run function canon:diana/par/step_closer
execute if score @s dv.timer matches 95 as @a[tag=dv_dtgt] at @s run playsound canon:diana.name hostile @s ^0.4 ^1.6 ^0.6 0.9 1
execute if score @s dv.timer matches 105 run function canon:diana/pose/req_back
execute if score @s dv.timer matches 105 run playsound canon:diana.crack hostile @a[tag=dv_dtgt] ~ ~1.6 ~ 1 0.7
execute if score @s dv.timer matches 138 run function canon:diana/pose/req_normal
execute if score @s dv.timer matches 138 run function canon:diana/expr/blank
execute if score @s dv.timer matches 150 as @a[tag=dv_dtgt] run function canon:diana/par/blink
execute if score @s dv.timer matches 156 run function canon:diana/par/lean_in
execute if score @s dv.timer matches 172 run function canon:diana/expr/grin
execute if score @s dv.timer matches 172 run playsound canon:diana.laugh hostile @a[tag=dv_dtgt] ~ ~2 ~ 1 0.9
execute if score @s dv.timer matches 176 run function canon:diana/pose/req_stretch_max
execute if score @s dv.timer matches 176 run function canon:diana/body/lean
execute if score @s dv.timer matches 200 run playsound canon:diana.breath hostile @a[tag=dv_dtgt] ~ ~2 ~ 1 0.8
execute if score @s dv.timer matches 236 run function canon:diana/expr/scream
execute if score @s dv.timer matches 238 as @a[tag=dv_dtgt] at @s run function canon:diana/par/end
execute if score @s dv.timer matches 238 run function canon:diana/vanish_quiet
