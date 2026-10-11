scoreboard players add @s dv.timer 1
execute unless score @s dv.posereq = @s dv.posecur run function canon:diana/pose/sync
scoreboard players set #dseen dv.tmp 0
execute if score #m2 dv.clock matches 0 run function canon:diana/look_check
execute if score #m2 dv.clock matches 1 if entity @s[tag=dv_dwasseen] run scoreboard players set #dseen dv.tmp 1
execute if score @s dv.state matches 1 run function canon:diana/s_far
execute if score @s dv.state matches 2 run function canon:diana/s_behind
execute if score @s dv.state matches 3 run function canon:diana/s_hunt
execute if score @s dv.state matches 4 run function canon:diana/s_par
execute if score @s dv.state matches 5 run function canon:diana/s_flash
execute if score @s dv.state matches 6 run function canon:diana/s_reveal
execute if score @s dv.state matches 7 run function canon:diana/s_walk
scoreboard players operation #id dv.tmp = @s dv.id
execute if score #m4 dv.clock matches 2 run function canon:diana/look_marker
