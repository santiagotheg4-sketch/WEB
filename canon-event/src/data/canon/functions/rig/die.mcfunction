tag @s add dv_dying
execute on passengers if entity @s[type=item_display] run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{scale:[0f,0f,0f]}}
particle minecraft:large_smoke ~ ~0.8 ~ 0.3 0.6 0.3 0.02 25 normal
particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.02 8 normal
execute if entity @s[tag=dv_devota] run function canon:devota/died
execute if entity @s[tag=dv_gato] run function canon:gato/died
