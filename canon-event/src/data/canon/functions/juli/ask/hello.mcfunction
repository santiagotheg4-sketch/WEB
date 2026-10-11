scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¿Has visto a Santi?","color":"#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 70
playsound canon:juli.hum ambient @a[distance=..16] ~ ~ ~ 0.5 1.1
