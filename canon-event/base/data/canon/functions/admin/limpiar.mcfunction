execute as @e[tag=dv_brain,distance=..64] at @s run function canon:rig/despawn
kill @e[type=item_display,tag=dv_part,distance=..64]
tellraw @s {"text":"[Canon Event] Criaturas cercanas eliminadas.","color":"dark_gray"}
