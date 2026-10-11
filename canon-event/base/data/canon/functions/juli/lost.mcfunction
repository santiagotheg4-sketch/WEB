scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"Otra vez te perdí…","color":"#9aa0a8"}',background:1342177280}
scoreboard players set @s dv.say 60
function canon:juli/expr/sad
execute as @a[tag=dv_jtgt] run scoreboard players set @s dv.juli 240
function canon:juli/start_bye
