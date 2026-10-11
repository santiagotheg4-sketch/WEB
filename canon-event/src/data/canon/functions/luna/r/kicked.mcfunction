scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_luna_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¡Auch! ¡Esa loca me pateó!","color":"#ff6b6b"}',background:1342177280}
scoreboard players set @s dv.say 70
playsound canon:ui.blip neutral @a[distance=..16] ~ ~0.8 ~ 0.45 1.8
playsound minecraft:entity.wolf.hurt neutral @a[distance=..16] ~ ~ ~ 1 1.7
scoreboard players set @s dv.mode 6
scoreboard players set @s dv.timer 0
