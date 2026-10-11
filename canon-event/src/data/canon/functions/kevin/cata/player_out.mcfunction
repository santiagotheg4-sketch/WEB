tag @s add dv_cout
tag @s remove dv_kpart
function canon:util/tp_return
effect give @s minecraft:darkness 3 0 true
stopsound @s ambient canon:cata.ambient
execute unless entity @a[tag=dv_kpart] run function canon:kevin/cata/win
