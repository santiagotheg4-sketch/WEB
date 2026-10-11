scoreboard players remove @s dv.timer2 1
execute if entity @a[distance=..1.7,gamemode=!spectator,gamemode=!creative] run function canon:mariana/kill
execute if score @s dv.timer2 matches ..0 run function canon:mariana/give_up
