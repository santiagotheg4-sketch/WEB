scoreboard players set @a[tag=dv_tgt] dv.near 0
execute at @a[tag=dv_tgt,limit=1] run tag @a[tag=!dv_tgt,distance=..3,limit=1,sort=nearest] add dv_rival
execute at @a[tag=dv_rival,limit=1] run tp @s ~ ~ ~
playsound canon:devota.scream hostile @a[distance=..48] ~ ~ ~ 1.5 1.2
function canon:devota/expr/scream
damage @a[tag=dv_rival,limit=1] 6 canon:abrazo by @s
execute as @a[tag=dv_rival] run function canon:fx/shake_small
tag @a remove dv_rival
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_dev_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¿Quién es ese? ¿POR QUÉ ESTÁ CONTIGO?","color":"#c43a4a"}',background:1342177280}
scoreboard players set @s dv.say 70
playsound canon:ui.blip neutral @a[distance=..16] ~ ~1.6 ~ 0.5 1.25
function canon:devota/blink_far
