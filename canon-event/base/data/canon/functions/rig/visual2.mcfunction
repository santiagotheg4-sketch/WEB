data modify storage canon:tmp r set from storage canon:tmp e.Rotation[0]
execute on passengers if entity @s[tag=dv_rot,tag=dv_ready] run data modify entity @s Rotation[0] set from storage canon:tmp r
execute unless entity @s[tag=dv_static] run function canon:rig/visual3
