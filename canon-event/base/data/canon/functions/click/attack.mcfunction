execute on attacker run tag @s add dv_talker
execute unless entity @a[tag=dv_talker] run tag @p add dv_talker
execute if entity @s[tag=dv_mari_click] run function canon:mariana/attacked
execute if entity @s[tag=dv_furn,tag=!dv_fijo] at @s run function canon:furn/remove
execute if entity @s[tag=dv_juli_click] run function canon:juli/attacked
execute if entity @s[tag=dv_dev_click] run function canon:devota/attacked
execute if entity @s[tag=dv_luna_click] run function canon:luna/attacked
execute if entity @s[tag=dv_npc_click] run function canon:npc2/attacked
data remove entity @s attack
tag @a[tag=dv_talker] remove dv_talker
