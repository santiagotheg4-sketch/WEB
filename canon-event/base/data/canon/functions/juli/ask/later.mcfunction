scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"Si lo ves… dile que lo sigo buscando.","color":"#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 70
function canon:juli/expr/sad
