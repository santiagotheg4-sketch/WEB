execute if entity @s[tag=dv_furn_on] as @e[type=item_display,tag=dv_mueble_rocola,distance=..0.6,limit=1,sort=nearest] run data merge entity @s {item:{tag:{CustomModelData:7320057}},brightness:{sky:0,block:0}}
execute unless entity @s[tag=dv_furn_on] as @e[type=item_display,tag=dv_mueble_rocola,distance=..0.6,limit=1,sort=nearest] run data merge entity @s {item:{tag:{CustomModelData:7320056}},brightness:{sky:0,block:13}}
function canon:furn/use_radio
