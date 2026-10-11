scoreboard players set #poster dv.puzzle 1
execute if score #d1 dv.puzzle matches 1 run data modify storage canon:tmp p1 set value "ROJO"
execute if score #d1 dv.puzzle matches 2 run data modify storage canon:tmp p1 set value "VERDE"
execute if score #d1 dv.puzzle matches 3 run data modify storage canon:tmp p1 set value "BLANCO"
execute if score #d2 dv.puzzle matches 1 run data modify storage canon:tmp p2 set value "ROJO"
execute if score #d2 dv.puzzle matches 2 run data modify storage canon:tmp p2 set value "VERDE"
execute if score #d2 dv.puzzle matches 3 run data modify storage canon:tmp p2 set value "BLANCO"
execute if score #d3 dv.puzzle matches 1 run data modify storage canon:tmp p3 set value "ROJO"
execute if score #d3 dv.puzzle matches 2 run data modify storage canon:tmp p3 set value "VERDE"
execute if score #d3 dv.puzzle matches 3 run data modify storage canon:tmp p3 set value "BLANCO"
execute if score #d4 dv.puzzle matches 1 run data modify storage canon:tmp p4 set value "ROJO"
execute if score #d4 dv.puzzle matches 2 run data modify storage canon:tmp p4 set value "VERDE"
execute if score #d4 dv.puzzle matches 3 run data modify storage canon:tmp p4 set value "BLANCO"
execute as @e[type=text_display,tag=dv_clue_disco] run function canon:escape/poster_apply
