scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_mari_bubble,distance=..40] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"…","color":"gray"}',background:1879048192}
function canon:mariana/bubble
function canon:mariana/turn_away
playsound minecraft:block.note_block.hat neutral @a[distance=..12] ~ ~ ~ 0.6 0.6
