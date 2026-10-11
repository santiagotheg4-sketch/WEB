execute if entity @e[type=zombie,tag=dv_juli,distance=..16] run function canon:luna/n/juli
execute if score @s dv.talkcd matches ..0 if entity @e[tag=dv_kevin,distance=..16] run function canon:luna/n/kevin
execute if score @s dv.talkcd matches ..0 if entity @e[type=zombie,tag=dv_mariana,distance=..12] run function canon:luna/n/mariana
execute if score @s dv.talkcd matches ..0 if entity @e[type=zombie,tag=dv_devota,distance=..20] if score #stage dv.dev matches 1..2 run function canon:luna/n/devota_kind
execute if score @s dv.talkcd matches ..0 if entity @e[type=zombie,tag=dv_devota,distance=..20] if score #stage dv.dev matches 3 run function canon:luna/n/devota_attached
