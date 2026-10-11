# una vez por tick por jugador
scoreboard players enable @s dv.kv
scoreboard players enable @s dv.jr
execute if score @s dv.kv matches 1.. run function canon:kevin/choice
execute if score @s dv.jr matches 1.. run function canon:casa/choice
execute if score @s dv.mst matches 1.. run function canon:nicolas/mined
execute if score @s dv.mds matches 1.. run function canon:nicolas/mined
execute if score #suenos dv.cfg matches 1 if data entity @s SleepingX run function canon:casa/sleeping
execute if score @s dv.kz matches 1.. unless data entity @s SleepingX run scoreboard players set @s dv.kz 0
execute if predicate canon:en_casa_sueno run function canon:casa/player
execute if score @s dv.sb matches 1.. unless predicate canon:en_casa_sueno run scoreboard players set @s dv.sb 0
scoreboard players remove @s[scores={dv.mus=1..}] dv.mus 1
