scoreboard players remove @s[scores={dv.sb=1..}] dv.sb 1
execute if score @s dv.mus matches ..0 run function canon:casa/music
execute if score @s dv.sb matches 1200 run title @s actionbar {"text": "La casa empieza a desdibujarse...", "color": "#cfcfcf", "italic": true}
execute if score @s dv.sb matches ..0 run function canon:casa/wake
execute unless entity @s[x=-40,y=0,z=-40,dx=96,dy=200,dz=96] run function canon:casa/lost
execute if entity @s[y=-64,dy=60] run function canon:casa/wake
execute if score #m200 dv.clock matches 0 run function canon:casa/ensure_juli
