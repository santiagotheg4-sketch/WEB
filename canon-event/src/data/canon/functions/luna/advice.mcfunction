scoreboard players set #adv dv.tmp 0
execute if score #stage dv.dev matches 4.. run scoreboard players set #adv dv.tmp 1
execute if score #adv dv.tmp matches 0 if score #stage dv.dev matches 2..3 if predicate canon:azar/50 run scoreboard players set #adv dv.tmp 2
execute if score #adv dv.tmp matches 0 if entity @a[scores={dv.dia=300..}] if predicate canon:azar/50 run scoreboard players set #adv dv.tmp 3
execute if score #adv dv.tmp matches 0 if predicate canon:de_noche if predicate canon:azar/1en3 run scoreboard players set #adv dv.tmp 4
execute if score #adv dv.tmp matches 0 if predicate canon:en_pueblo run scoreboard players set #adv dv.tmp 5
execute if score #adv dv.tmp matches 0 if score #kdays dv.dev matches 1.. run scoreboard players set #adv dv.tmp 7
execute if score #adv dv.tmp matches 1 run function canon:luna/adv/devota_bad
execute if score #adv dv.tmp matches 2 run function canon:luna/adv/devota_kind
execute if score #adv dv.tmp matches 3 run function canon:luna/adv/diana
execute if score #adv dv.tmp matches 4 run function canon:luna/adv/night
execute if score #adv dv.tmp matches 5 run function canon:luna/adv/town
execute if score #adv dv.tmp matches 7 run function canon:luna/adv/kevin3
execute if score #adv dv.tmp matches 0 run function canon:luna/say_general
scoreboard players set @s dv.mode 5
scoreboard players set @s dv.timer 30
