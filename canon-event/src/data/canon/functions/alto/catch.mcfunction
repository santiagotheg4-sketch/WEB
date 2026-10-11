playsound canon:alto.aparece master @a[tag=dv_wtgt] ~ ~ ~ 1 1
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
damage @a[tag=dv_wtgt,limit=1] 10 minecraft:mob_attack by @s
effect give @a[tag=dv_wtgt] minecraft:blindness 3 0 true
tellraw @a[tag=dv_wtgt] {"text":"No tenía cara. Pero sonreía.","color":"#d8d8d8","italic":true}
tag @a[tag=dv_wtgt] remove dv_kpart
scoreboard players set @s dv.timer 0
execute at @a[tag=dv_kpart,limit=1,sort=random] positioned ^ ^ ^-24 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
