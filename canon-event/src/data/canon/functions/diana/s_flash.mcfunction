execute if score #m4 dv.clock matches 0 run function canon:diana/face
execute if score @s dv.timer matches 1 run function canon:diana/expr/grin
execute if score @s dv.timer matches 1 run playsound canon:diana.flicker master @a[tag=dv_dtgt] ~ ~ ~ 0.7 1
execute if score @s dv.timer matches 1 if score #susto dv.cfg matches 1 run effect give @a[tag=dv_dtgt] minecraft:darkness 3 0 true
execute if score @s dv.timer matches 12.. if score #dseen dv.tmp matches 1 if predicate canon:azar/1en3 as @a[tag=dv_dtgt] at @s run function canon:diana/jumpscare
execute if score @s dv.timer matches 12.. if score #dseen dv.tmp matches 1 run function canon:diana/vanish_quiet
execute if score @s dv.state matches 5 if score @s dv.timer matches 40.. run function canon:diana/vanish_quiet
