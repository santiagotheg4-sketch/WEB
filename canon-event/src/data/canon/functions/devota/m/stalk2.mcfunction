execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score #seen dv.tmp matches 0 if score @s dv.watch matches 1.. run function canon:devota/unwatched
execute if score @s dv.watch matches 30 run function canon:devota/pose/req_tilt
execute if score @s dv.watch matches 60 run function canon:devota/expr/grin
execute if score @s dv.watch matches 60 run playsound canon:devota.giggle hostile @a[distance=..24] ~ ~ ~ 0.7 1.3
execute if score @s dv.watch matches 160.. run function canon:devota/vanish_seen
scoreboard players remove @s[scores={dv.lose=1..}] dv.lose 1
execute if score #seen dv.tmp matches 0 if score @s dv.lose matches ..0 if score #d dv.tmp matches 16.. run function canon:devota/blink_closer
execute if score #seen dv.tmp matches 0 if score @s dv.lose matches ..0 if score #d dv.tmp matches 8 run function canon:devota/blink_behind
execute if score #m200 dv.clock matches 50 if predicate canon:azar/1en3 run function canon:devota/talk_line
execute if score #m40 dv.clock matches 20 run function canon:devota/rival_check
execute if score @s dv.timer2 matches ..0 run function canon:devota/start_leave
