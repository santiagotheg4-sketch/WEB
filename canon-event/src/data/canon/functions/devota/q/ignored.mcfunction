scoreboard players remove #sane dv.dev 30
function canon:devota/expr/cry
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_dev_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¿Por qué no me contestas?","color":"#d77a8a"}',background:1342177280}
scoreboard players set @s dv.say 70
playsound canon:ui.blip neutral @a[distance=..16] ~ ~1.6 ~ 0.5 1.25
