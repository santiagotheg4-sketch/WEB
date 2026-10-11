scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a if score @s dv.pid = #tgt dv.tmp run tag @s add dv_dtgt
execute if score @s dv.state matches 3 if score #m20 dv.clock matches 0 run function canon:diana/retarget_near
execute unless entity @a[tag=dv_dtgt,distance=..110] unless score @s dv.state matches 4 run function canon:diana/retarget_near
execute unless entity @a[tag=dv_dtgt,distance=..110] run function canon:diana/gone
execute if entity @a[tag=dv_dtgt,distance=..110] run function canon:diana/think
tag @a[tag=dv_dtgt] remove dv_dtgt
