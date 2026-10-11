execute if entity @s[tag=dv_furn_tv] run loot spawn ~ ~0.4 ~ loot canon:items/m_tv
execute if entity @s[tag=dv_furn_radio_antigua] run loot spawn ~ ~0.4 ~ loot canon:items/m_radio
execute if entity @s[tag=dv_furn_rocola] run loot spawn ~ ~0.4 ~ loot canon:items/m_rocola
execute if entity @s[tag=dv_furn_nevera] run loot spawn ~ ~0.4 ~ loot canon:items/m_nevera
execute if entity @s[tag=dv_furn_lavadora] run loot spawn ~ ~0.4 ~ loot canon:items/m_lavadora
execute if entity @s[tag=dv_furn_expendedora] run loot spawn ~ ~0.4 ~ loot canon:items/m_expendedora
execute if entity @s[tag=dv_furn_telefono] run loot spawn ~ ~0.4 ~ loot canon:items/m_telefono
execute if entity @s[tag=dv_furn_lampara] run loot spawn ~ ~0.4 ~ loot canon:items/m_lampara
execute if entity @s[tag=dv_furn_sillon] run loot spawn ~ ~0.4 ~ loot canon:items/m_sillon
execute if entity @s[tag=dv_furn_farola] run loot spawn ~ ~0.4 ~ loot canon:items/m_farola
kill @e[type=item_display,tag=dv_mueble,distance=..0.6,limit=1,sort=nearest]
execute if block ~ ~ ~ minecraft:barrier run setblock ~ ~ ~ minecraft:air
execute if block ~ ~1 ~ minecraft:barrier run setblock ~ ~1 ~ minecraft:air
execute if block ~ ~1 ~ minecraft:light run setblock ~ ~1 ~ minecraft:air
execute if block ~ ~2 ~ minecraft:light run setblock ~ ~2 ~ minecraft:air
playsound minecraft:block.wood.break block @a[distance=..16] ~ ~ ~ 1 0.8
kill @s
