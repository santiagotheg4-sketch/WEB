scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"Este lugar es de los dos. Bueno, ahora también un poco tuyo.","color":"#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 90
scoreboard players set #k dv.tmp 1
