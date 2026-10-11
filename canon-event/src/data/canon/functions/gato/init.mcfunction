function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players set @s dv.cmd 7320037
attribute @s minecraft:generic.max_health base set 14
data merge entity @s {Health:14f}
attribute @s minecraft:generic.movement_speed base set 0.34
attribute @s minecraft:generic.attack_damage base set 3
