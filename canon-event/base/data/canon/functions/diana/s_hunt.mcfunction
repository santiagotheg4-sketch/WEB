scoreboard players remove @s dv.timer2 1
execute if score @s dv.timer matches 1 run function canon:diana/pose/req_crawl
execute if score @s dv.timer matches 1 run function canon:diana/expr/crawl
execute if score @s dv.timer matches 1 run playsound canon:diana.scream hostile @a[distance=..64] ~ ~ ~ 2 0.9
execute if score @s dv.timer matches 1 if score #susto dv.cfg matches 1 run effect give @a[tag=dv_dtgt] minecraft:darkness 4 0 true
execute if score @s dv.timer matches ..20 run function canon:diana/face
execute if score @s dv.timer matches 21.. run function canon:diana/hunt_move
execute if score #m40 dv.clock matches 0 run playsound canon:diana.crawl hostile @a[distance=..32] ~ ~ ~ 1 1
execute if score #m40 dv.clock matches 20 if predicate canon:azar/1en3 run playsound canon:diana.scream hostile @a[distance=..48] ~ ~ ~ 1.4 1.2
execute if score #m40 dv.clock matches 10 if score #susto dv.cfg matches 1 run playsound canon:diana.flicker master @a[tag=dv_dtgt] ~ ~ ~ 0.5 1
execute if score #m40 dv.clock matches 10 if score #susto dv.cfg matches 1 run effect give @a[tag=dv_dtgt] minecraft:darkness 2 0 true
execute if score @s dv.state matches 3 if entity @a[distance=..1.6,gamemode=!spectator,gamemode=!creative] run function canon:diana/catch
execute if score @s dv.state matches 3 if score @s dv.timer2 matches ..0 run function canon:diana/hunt_end
