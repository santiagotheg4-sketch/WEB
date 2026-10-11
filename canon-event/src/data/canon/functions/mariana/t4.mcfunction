scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_mari_bubble,distance=..40] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"…","color":"dark_red"}',background:1879048192}
function canon:mariana/bubble
function canon:mariana/turn_away
scoreboard players set @s dv.state 1
scoreboard players set @s dv.timer2 16
effect give @a[tag=dv_talker] minecraft:darkness 2 0 true
playsound canon:fx.sub_hit ambient @a[tag=dv_talker] ~ ~ ~ 0.5 1.4
