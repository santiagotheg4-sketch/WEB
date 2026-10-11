scoreboard players set #rdy dv.tmp 0
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run scoreboard players set #rdy dv.tmp 1
execute if score #rdy dv.tmp matches 1 if score @s dv.posereq matches 0 run function canon:diana/pose/normal
execute if score #rdy dv.tmp matches 1 if score @s dv.posereq matches 1 run function canon:diana/pose/crawl
execute if score #rdy dv.tmp matches 1 if score @s dv.posereq matches 2 run function canon:diana/pose/back
execute if score #rdy dv.tmp matches 1 if score @s dv.posereq matches 3 run function canon:diana/pose/tilt
execute if score #rdy dv.tmp matches 1 if score @s dv.posereq matches 4 run function canon:diana/pose/stretch
execute if score #rdy dv.tmp matches 1 if score @s dv.posereq matches 5 run function canon:diana/pose/stretch_max
execute if score #rdy dv.tmp matches 1 if score @s dv.posereq matches 6 run function canon:diana/pose/snap
