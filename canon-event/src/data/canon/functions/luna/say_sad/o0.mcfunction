scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_luna_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¿Por qué?","color":"#9aa0a8"}',background:1342177280}
scoreboard players set @s dv.say 60
playsound canon:ui.blip neutral @a[distance=..16] ~ ~0.8 ~ 0.45 1.8
scoreboard players set #k dv.tmp 1
