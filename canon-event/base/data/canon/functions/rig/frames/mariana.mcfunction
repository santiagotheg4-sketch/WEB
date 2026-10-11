execute if score @s dv.state matches 3 run function canon:rig/frames/walker
execute if score @s dv.state matches 3 if score #moving dv.tmp matches 0 run scoreboard players set #frame dv.tmp 7
execute unless score @s dv.state matches 3 if entity @s[tag=dv_bailando] run function canon:rig/frames/mariana_dance
execute unless score @s dv.state matches 3 unless entity @s[tag=dv_bailando] run function canon:rig/frames/mariana_still
execute if entity @s[tag=dv_stare] run scoreboard players set #frame dv.tmp 7
