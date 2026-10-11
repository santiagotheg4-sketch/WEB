scoreboard players set #fd dv.tmp 4
execute if score #es dv.tmp matches 2 run scoreboard players set #fd dv.tmp 5
execute if score #es dv.tmp matches 3 run scoreboard players set #fd dv.tmp 3
execute if score #es dv.tmp matches 4 run scoreboard players set #fd dv.tmp 2
scoreboard players remove @s[scores={dv.jeal=1..}] dv.jeal 1
execute if score @s dv.jeal matches 0 run tag @s remove dv_waving
scoreboard players set #far dv.tmp 0
execute if entity @a[tag=dv_tgt,distance=7..] run scoreboard players set #far dv.tmp 1
execute if score #fd dv.tmp matches 2 if entity @a[tag=dv_tgt,distance=3.5..] run scoreboard players set #far dv.tmp 1
execute if score #fd dv.tmp matches 3 if entity @a[tag=dv_tgt,distance=4.5..] run scoreboard players set #far dv.tmp 1
execute if score #fd dv.tmp matches 5 unless entity @a[tag=dv_tgt,distance=..6.5] run scoreboard players set #far dv.tmp 1
execute if score #far dv.tmp matches 1 run function canon:devota/clear_acts
execute if score #far dv.tmp matches 1 unless entity @a[tag=dv_tgt,distance=..14] run function canon:devota/run_to
execute if score #far dv.tmp matches 1 if entity @a[tag=dv_tgt,distance=..14] run function canon:devota/walk_to
execute if score #far dv.tmp matches 0 if score #m4 dv.clock matches 0 unless entity @s[tag=dv_sitting] run function canon:devota/face
execute if score #far dv.tmp matches 0 run scoreboard players remove @s dv.idle 1
execute if score @s dv.idle matches ..0 run function canon:devota/idle_act
execute if score #m40 dv.clock matches 7 run function canon:devota/protect_check
execute if score #es dv.tmp matches 3.. if score #m20 dv.clock matches 9 run function canon:devota/runaway_check
execute if score #es dv.tmp matches 4 if score #m20 dv.clock matches 13 run function canon:devota/jealous_check
execute if score #es dv.tmp matches 4 if score #seen dv.tmp matches 0 if score #d dv.tmp matches 16.. if predicate canon:azar/1en200 run function canon:devota/blink_behind
execute if score #es dv.tmp matches 4 if score #seen dv.tmp matches 1 run function canon:devota/expr/stare
execute if score @s dv.timer2 matches ..0 run function canon:devota/start_leave
execute if score #es dv.tmp matches 5.. run function canon:devota/turn_dangerous
