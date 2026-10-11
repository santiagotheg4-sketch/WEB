scoreboard players remove #sane dv.dev 120
scoreboard players remove #love dv.dev 30
playsound canon:devota.whisper hostile @a[distance=..16] ~ ~ ~ 1 0.6
function canon:devota/expr/cry
function canon:devota/clear_acts
tag @s add dv_covering
function canon:luna/react/devota_hit
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_dev_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¿Por qué me haces esto?","color":"#d77a8a"}',background:1342177280}
scoreboard players set @s dv.say 70
playsound canon:ui.blip neutral @a[distance=..16] ~ ~1.6 ~ 0.5 1.25
scoreboard players set @s dv.mode 3
scoreboard players set @s dv.timer 30
