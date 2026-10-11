scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_luna_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¡Ese chico de negro huele a rabia! ¡Grrr! ¡Corre!","color":"#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 60
function canon:luna/bark2
scoreboard players set @s dv.talkcd 600
