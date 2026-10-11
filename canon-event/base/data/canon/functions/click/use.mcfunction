execute on target run tag @s add dv_talker
execute unless entity @a[tag=dv_talker] run tag @p add dv_talker
execute if entity @s[tag=dv_mari_click] run function canon:mariana/clicked
execute if entity @s[tag=dv_furn] at @s run function canon:furn/clicked
execute if entity @s[tag=dv_fusebox] at @s run function canon:puzzle/fusebox
execute if entity @s[tag=dv_juli_click] run function canon:juli/clicked
execute if entity @s[tag=dv_dev_click] run function canon:devota/clicked
execute if entity @s[tag=dv_luna_click] run function canon:luna/clicked
execute if entity @s[tag=dv_npc_click] run function canon:npc2/clicked
execute if entity @s[tag=dv_puerta_sueno] run function canon:sueno/door_used
data remove entity @s interaction
tag @a[tag=dv_talker] remove dv_talker
