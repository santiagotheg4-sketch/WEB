scoreboard players set #sg dv.tmp 0
execute if score #senales dv.cfg matches 1 if score @s dv.dia matches 350.. if predicate canon:azar/1en8 run scoreboard players set #sg dv.tmp 1
execute if score #sg dv.tmp matches 0 if score #senales dv.cfg matches 1 if score @s dv.dia matches 200.. if predicate canon:azar/1en6 run scoreboard players set #sg dv.tmp 2
execute if score #sg dv.tmp matches 0 if score @s dv.dia matches 250.. unless score @s dv.dleft matches 1.. if predicate canon:azar/1en8 run scoreboard players set #sg dv.tmp 3
execute if score #sg dv.tmp matches 0 if score @s dv.dia matches 200.. if predicate canon:azar/1en8 run scoreboard players set #sg dv.tmp 4
execute if score #sg dv.tmp matches 1 run function canon:diana/sign/place
execute if score #sg dv.tmp matches 2 run function canon:diana/sign/torches
execute if score #sg dv.tmp matches 3 run function canon:diana/sign/join
execute if score #sg dv.tmp matches 4 run function canon:diana/sign/hair
execute if score #sg dv.tmp matches 0 run function canon:diana/sign/basic
