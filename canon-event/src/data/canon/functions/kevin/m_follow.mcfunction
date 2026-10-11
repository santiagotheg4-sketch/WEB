execute if entity @a[tag=dv_wtgt,distance=4..] run function canon:x/walk
execute if entity @a[tag=dv_wtgt,distance=26..] at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-3 run function canon:kevin/catch_up
execute if entity @a[tag=dv_wtgt,distance=..4] if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players remove @s dv.timer 1
execute if score #kprog dv.dev matches 5 run scoreboard players remove @s dv.timer 1
execute if score @s dv.timer matches ..0 if score @s dv.say matches ..0 run function canon:kevin/joke_auto
