tag @e[type=item_display,tag=dv_part] add dv_orphan
execute as @e[tag=dv_brain] on passengers run tag @s remove dv_orphan
kill @e[type=item_display,tag=dv_orphan]
tag @e[tag=dv_link] add dv_orphan
execute as @e[tag=dv_brain] run function canon:rig/claim_links
kill @e[tag=dv_link,tag=dv_orphan]
