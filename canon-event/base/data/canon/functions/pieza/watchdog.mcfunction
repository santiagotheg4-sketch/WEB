scoreboard players set #n dv.tmp 0
execute as @a run function canon:pieza/count_bateria
execute in canon:valle_quieto if entity @e[type=item,tag=dv_pieza_bateria] run scoreboard players set #n dv.tmp 1
execute if score #n dv.tmp matches 0 unless score #p_bat dv.parts matches 1 in canon:valle_quieto as @e[type=marker,tag=dv_ped_bateria,limit=1] at @s run function canon:pieza/spawn_bateria
scoreboard players set #n dv.tmp 0
execute as @a run function canon:pieza/count_gasolina
execute in canon:valle_quieto if entity @e[type=item,tag=dv_pieza_gasolina] run scoreboard players set #n dv.tmp 1
execute if score #n dv.tmp matches 0 unless score #p_gas dv.parts matches 1 in canon:valle_quieto as @e[type=marker,tag=dv_ped_gasolina,limit=1] at @s run function canon:pieza/spawn_gasolina
scoreboard players set #n dv.tmp 0
execute as @a run function canon:pieza/count_bujias
execute in canon:valle_quieto if entity @e[type=item,tag=dv_pieza_bujias] run scoreboard players set #n dv.tmp 1
execute if score #n dv.tmp matches 0 unless score #p_buj dv.parts matches 1 in canon:valle_quieto as @e[type=marker,tag=dv_ped_bujias,limit=1] at @s run function canon:pieza/spawn_bujias
scoreboard players set #n dv.tmp 0
execute as @a run function canon:pieza/count_llaves
execute in canon:valle_quieto if entity @e[type=item,tag=dv_pieza_llaves] run scoreboard players set #n dv.tmp 1
execute if score #n dv.tmp matches 0 unless score #p_lla dv.parts matches 1 in canon:valle_quieto as @e[type=marker,tag=dv_ped_llaves,limit=1] at @s run function canon:pieza/spawn_llaves
scoreboard players set #n dv.tmp 0
execute as @a run function canon:pieza/count_fusible
execute in canon:valle_quieto if entity @e[type=item,tag=dv_pieza_fusible] run scoreboard players set #n dv.tmp 1
execute if score #n dv.tmp matches 0 if score #sol3 dv.puzzle matches 0 in canon:valle_quieto as @e[type=marker,tag=dv_ped_fusible,limit=1] at @s run function canon:pieza/spawn_fusible
