scoreboard players remove #sane dv.dev 15
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_dev_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¿Y yo qué? A mí nunca me acaricias así.","color":"#d77a8a"}',background:1342177280}
scoreboard players set @s dv.say 60
playsound canon:ui.blip neutral @a[distance=..16] ~ ~0.8 ~ 0.45 1.8
