data modify storage canon:tmp e set from entity @s
execute store result score @s dv.hp run data get storage canon:tmp e.Health 10
execute if score @s dv.hp < @s dv.hpold run function canon:rig/hurt
scoreboard players operation @s dv.hpold = @s dv.hp
execute if score @s dv.hp matches ..0 unless entity @s[tag=dv_dying] run function canon:rig/die
execute if score @s dv.flash matches 1.. run scoreboard players remove @s dv.flash 1
execute if score @s dv.flash matches 0 if entity @s[tag=dv_flashing] run function canon:rig/unflash
execute unless entity @s[tag=dv_dying] run function canon:rig/visual2
