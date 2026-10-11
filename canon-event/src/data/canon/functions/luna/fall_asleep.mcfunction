scoreboard players set @s dv.mode 2
scoreboard players set @s dv.timer 0
playsound minecraft:entity.wolf.whine neutral @a[distance=..12] ~ ~ ~ 0.4 1.4
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_luna_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"Zzz…","color":"#9ab8f0"}',background:1342177280}
scoreboard players set @s dv.say 80
playsound canon:ui.blip neutral @a[distance=..16] ~ ~0.8 ~ 0.45 1.8
