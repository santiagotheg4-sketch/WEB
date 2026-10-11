scoreboard players add @s dv.lose 1
execute if score #heard dv.tmp matches 1 run scoreboard players set @s dv.lose 0
execute if entity @a[distance=..8,gamemode=!spectator,gamemode=!creative] run scoreboard players set @s dv.lose 0
scoreboard players remove @s[scores={dv.timer2=1..}] dv.timer2 1
execute if entity @a[distance=..2.4,gamemode=!spectator,gamemode=!creative] if score @s dv.jeal matches ..0 run function canon:devota/embrace
scoreboard players remove @s[scores={dv.jeal=1..}] dv.jeal 1
execute if score @s dv.timer matches 40 run function canon:devota/expr/grin
execute if score @s dv.lose matches 220.. if score #es dv.tmp matches ..5 run function canon:devota/start_search
execute if score @s dv.lose matches 400.. if score #es dv.tmp matches 6 run function canon:devota/blink_closer
execute if score @s dv.lose matches 400.. run scoreboard players set @s dv.lose 0
execute if score @s dv.timer matches 1200.. run function canon:devota/start_search
execute if predicate canon:azar/1en40 run playsound canon:devota.step hostile @a[distance=..20] ~ ~ ~ 0.8 1
