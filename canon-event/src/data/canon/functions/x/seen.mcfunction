scoreboard players set #seen dv.tmp 0
tag @s add dv_lookme
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^4 if entity @e[tag=dv_lookme,distance=..2.6] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^8 if entity @e[tag=dv_lookme,distance=..4] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^14 if entity @e[tag=dv_lookme,distance=..6] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^20 if entity @e[tag=dv_lookme,distance=..8] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^28 if entity @e[tag=dv_lookme,distance=..10] run scoreboard players set #seen dv.tmp 1
execute as @a[tag=dv_lookers] at @s anchored eyes positioned ^ ^ ^38 if entity @e[tag=dv_lookme,distance=..13] run scoreboard players set #seen dv.tmp 1
tag @s remove dv_lookme
