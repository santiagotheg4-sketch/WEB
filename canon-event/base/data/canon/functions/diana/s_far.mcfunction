execute if score #m4 dv.clock matches 0 run function canon:diana/face
execute if score #dseen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score @s dv.watch matches 7.. run function canon:diana/far_seen
execute if score @s dv.state matches 1 if entity @a[tag=dv_dtgt,distance=..18] run function canon:diana/far_seen
execute if score @s dv.state matches 1 if score @s dv.timer matches 600.. run function canon:diana/vanish_quiet
