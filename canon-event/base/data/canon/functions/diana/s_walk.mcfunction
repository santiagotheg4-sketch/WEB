execute rotated ~ 0 positioned ^ ^ ^0.09 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
execute if score #dseen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score @s dv.watch matches 10.. run function canon:diana/far_seen
execute if score @s dv.state matches 7 if score @s dv.timer matches 260.. run function canon:diana/vanish_quiet
