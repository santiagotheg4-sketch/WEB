execute if score #m4 dv.clock matches 0 run function canon:diana/face
execute if score @s dv.timer matches 1 run playsound canon:diana.crack hostile @a[tag=dv_dtgt] ~ ~1 ~ 0.9 1
execute if score @s dv.timer matches 2 run function canon:diana/pose/req_back
execute if score @s dv.timer matches 2 run function canon:diana/expr/twisted
execute if score @s dv.timer matches 4 if score #susto dv.cfg matches 1 run effect give @a[tag=dv_dtgt] minecraft:darkness 6 0 true
execute if score #m40 dv.clock matches 0 run playsound canon:diana.breath hostile @a[tag=dv_dtgt] ~ ~1.5 ~ 0.6 1
execute if score #m20 dv.clock matches 5 if predicate canon:azar/1en3 run playsound canon:diana.crack hostile @a[tag=dv_dtgt] ~ ~1.4 ~ 0.6 1.2
execute if score @s dv.timer matches 4.. if score #dseen dv.tmp matches 1 run function canon:diana/reveal_start
execute if score @s dv.state matches 2 if score #m4 dv.clock matches 1 if entity @a[tag=dv_dtgt,distance=3.6..] run function canon:diana/behind_follow
execute if score @s dv.state matches 2 if score @s dv.timer matches 90 run playsound canon:diana.name hostile @a[tag=dv_dtgt] ~ ~1.6 ~ 0.8 1
execute if score @s dv.state matches 2 if score @s dv.timer matches 170.. run function canon:diana/behind_leave
