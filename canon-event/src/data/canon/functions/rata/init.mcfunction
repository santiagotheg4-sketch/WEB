function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320047
attribute @s minecraft:generic.max_health base set 6
data merge entity @s {Health:6f}
