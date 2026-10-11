execute if score #clues dv.puzzle matches 0 in canon:valle_quieto if entity @e[type=text_display,tag=dv_clue_1] run function canon:escape/set_clues
execute if score #poster dv.puzzle matches 0 in canon:valle_quieto if entity @e[type=text_display,tag=dv_clue_disco] run function canon:escape/set_poster
execute if score #rs_pending dv.puzzle matches 1 in canon:valle_quieto if loaded -2 58 -37 if loaded -49 64 -42 if loaded 40 64 -90 if loaded -40 64 -87 run function canon:escape/apply_reset
execute if score #car_pend dv.puzzle matches 1 in canon:valle_quieto as @e[type=marker,tag=dv_car_home,limit=1] at @s unless entity @e[type=horse,tag=dv_car_town] run function canon:car/spawn_town_here
execute in canon:valle_quieto as @e[type=item,tag=dv_pieza] at @s run particle minecraft:end_rod ~ ~0.4 ~ 0.1 0.2 0.1 0.01 2 normal
execute if score #m200 dv.clock matches 0 run function canon:pieza/watchdog
