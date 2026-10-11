# poses de la segunda oleada
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if entity @s[tag=dv_kdance] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 3
execute if entity @s[tag=dv_kdance] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 4
execute if entity @s[tag=dv_klaugh] run scoreboard players set #frame dv.tmp 5
execute if entity @s[tag=dv_koffer] run scoreboard players set #frame dv.tmp 6
execute if entity @s[tag=dv_nreach] run scoreboard players set #frame dv.tmp 3
execute if entity @s[tag=dv_areach] run scoreboard players set #frame dv.tmp 3
execute if entity @s[tag=dv_fiestero] run function canon:rig/frames/fiestero
execute if entity @s[tag=dv_miron,tag=dv_mpeek] run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_masa] run function canon:rig/frames/masa
