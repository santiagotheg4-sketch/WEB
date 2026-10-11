execute unless score @s dv.joined matches 1 run function canon:player/first_join
execute unless score @s dv.pid matches 1.. run function canon:player/assign_pid
execute if score @s dv.leave matches 1.. run function canon:player/rejoin
execute if score @s dv.death matches 1.. run function canon:player/died
function canon:player/noise
execute if score @s dv.use matches 1.. run function canon:items/use
scoreboard players remove @s[scores={dv.cool=1..}] dv.cool 1
execute if score @s dv.deseo matches 1.. run function canon:wish/choose
execute if score @s dv.menu matches 1.. run function canon:menu/trigger
scoreboard players enable @s dv.menu
execute if score #m2 dv.clock matches 0 if entity @e[type=zombie,tag=dv_devota,distance=..48] run function canon:player/look
execute if score #m2 dv.clock matches 0 unless entity @e[type=zombie,tag=dv_devota,distance=..48] run scoreboard players set @s dv.seen 0
execute if predicate canon:en_pueblo run function canon:town/player_in
execute if score @s dv.town matches 1 unless predicate canon:en_pueblo run function canon:town/player_left
execute if score @s dv.travel matches 1.. run function canon:travel/tick
execute if score @s dv.inv matches 1.. run function canon:wish/inv_tick
execute if score @s dv.sleep matches 1.. run scoreboard players remove @s dv.sleep 1
execute if score @s dv.pill matches 1.. run function canon:items/pill_tick
execute if score @s dv.rain matches 1.. run function canon:wish/rain_tick
execute if score #m10 dv.clock matches 0 run function canon:hud/maybe
execute if predicate canon:en_carro run function canon:car/rider_tick
execute if score #diana dv.cfg matches 1 if predicate canon:en_superficie run function canon:diana/player
execute if score @s dv.par matches 1.. run function canon:diana/par/tick
execute if score @s dv.lint matches 1 run function canon:items/linterna/tick
execute if score #juli dv.cfg matches 1 if score #m20 dv.clock matches 11 if predicate canon:en_superficie run function canon:juli/player
execute if predicate canon:en_sueno run function canon:sueno/player
execute if score @s dv.escena matches 1.. unless entity @e[type=zombie,tag=dv_juli,distance=..16] run function canon:juli/scene/unlock
execute if score @s dv.resp matches 1.. run function canon:devota/q/answer
execute if score @s dv.shake matches 1.. run function canon:fx/shake_tick
function canon:extra/player
