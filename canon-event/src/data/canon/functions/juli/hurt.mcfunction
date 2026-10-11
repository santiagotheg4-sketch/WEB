scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"…","color":"#9aa0a8"}',background:1342177280}
scoreboard players set @s dv.say 40
function canon:juli/expr/sad
execute unless score @s dv.state matches 3..4 run function canon:juli/start_bye
