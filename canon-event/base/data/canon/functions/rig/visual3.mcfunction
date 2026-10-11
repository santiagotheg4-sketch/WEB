execute store result score #mx dv.tmp run data get storage canon:tmp e.Motion[0] 1000
execute store result score #mz dv.tmp run data get storage canon:tmp e.Motion[2] 1000
execute if score #mx dv.tmp matches ..-1 run scoreboard players operation #mx dv.tmp *= #-1 dv.math
execute if score #mz dv.tmp matches ..-1 run scoreboard players operation #mz dv.tmp *= #-1 dv.math
scoreboard players operation #mx dv.tmp += #mz dv.tmp
scoreboard players set #moving dv.tmp 0
execute if score #mx dv.tmp matches 22.. run scoreboard players set #moving dv.tmp 1
scoreboard players add @s dv.anim 1
scoreboard players set #frame dv.tmp 0
execute if entity @s[tag=dv_walker] run function canon:rig/frames/walker
execute if entity @s[tag=dv_quad] run function canon:rig/frames/quad
execute if entity @s[tag=dv_bird] run function canon:rig/frames/bird
execute if entity @s[tag=dv_devota] run function canon:rig/frames/devota
execute if entity @s[tag=dv_mariana] run function canon:rig/frames/mariana
execute if entity @s[tag=dv_diana] run function canon:rig/frames/diana
execute if entity @s[tag=dv_juli] run function canon:rig/frames/juli
execute if entity @s[tag=dv_luna] run function canon:rig/frames/luna
execute if entity @s[tag=dv_rigx] run function canon:rig/frames/extra
execute unless score #frame dv.tmp = @s dv.frame run function canon:rig/apply_frame
