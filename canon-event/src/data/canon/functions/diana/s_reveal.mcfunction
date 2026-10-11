execute if score #m2 dv.clock matches 0 run function canon:diana/face
execute if score @s dv.timer matches 5 as @a[tag=dv_dtgt] at @s run function canon:diana/jumpscare
execute if score @s dv.timer matches 5 as @a[distance=..10,tag=!dv_dtgt] at @s run playsound canon:diana.scream master @s ~ ~ ~ 0.8 1
execute if score @s dv.timer matches 5 as @a[distance=..10] run function canon:fx/shake_big
execute if score @s dv.timer matches 5 run damage @a[tag=dv_dtgt,limit=1] 4 canon:diana by @s
execute if score @s dv.timer matches 5 as @a[tag=dv_dtgt] run function canon:diana/fed_small
execute if score @s dv.timer matches 6.. run function canon:diana/vanish
