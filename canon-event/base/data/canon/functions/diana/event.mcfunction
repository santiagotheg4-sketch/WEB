scoreboard players set #ev dv.tmp 0
execute if score @s dv.dia matches 700.. if score @s dv.dhunt matches ..0 if predicate canon:azar/1en4 run scoreboard players set #ev dv.tmp 4
execute if score #ev dv.tmp matches 0 if score @s dv.dia matches 450.. if predicate canon:azar/1en3 run scoreboard players set #ev dv.tmp 3
execute if score #ev dv.tmp matches 0 if score @s dv.dia matches 250.. if predicate canon:azar/50 run scoreboard players set #ev dv.tmp 2
execute if score #ev dv.tmp matches 0 run scoreboard players set #ev dv.tmp 1
execute if score #ev dv.tmp matches 4 run function canon:diana/ev/hunt
execute if score #ev dv.tmp matches 3 run function canon:diana/ev/near
execute if score #ev dv.tmp matches 2 run function canon:diana/ev/far
execute if score #ev dv.tmp matches 1 run function canon:diana/ev/sign
scoreboard players set @s dv.dcd 40
execute if predicate canon:azar/50 run scoreboard players add @s dv.dcd 25
execute if predicate canon:azar/50 run scoreboard players add @s dv.dcd 20
execute if score @s dv.dia matches 450.. run scoreboard players remove @s dv.dcd 15
