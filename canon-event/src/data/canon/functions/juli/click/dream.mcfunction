scoreboard players add @s dv.jline 1
execute if score @s dv.jline matches 7.. run scoreboard players set @s dv.jline 1
execute if entity @a[tag=dv_talker,tag=dv_santi] if score @s dv.jline matches 1 run function canon:juli/dream/santi_1
execute if entity @a[tag=dv_talker,tag=dv_santi] if score @s dv.jline matches 2 run function canon:juli/dream/santi_2
execute if entity @a[tag=dv_talker,tag=dv_santi] if score @s dv.jline matches 3 run function canon:juli/dream/santi_3
execute if entity @a[tag=dv_talker,tag=dv_santi] if score @s dv.jline matches 4 run function canon:juli/dream/santi_4
execute if entity @a[tag=dv_talker,tag=dv_santi] if score @s dv.jline matches 5 run function canon:juli/dream/santi_5
execute if entity @a[tag=dv_talker,tag=dv_santi] if score @s dv.jline matches 6 run function canon:juli/dream/santi_6
execute unless entity @a[tag=dv_talker,tag=dv_santi] run function canon:juli/click/dream_others
function canon:juli/expr/soft
