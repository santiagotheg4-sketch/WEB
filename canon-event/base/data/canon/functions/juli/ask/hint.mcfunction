scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"Está cerca… ¿verdad? Gracias.","color":"#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 70
function canon:juli/expr/soft
execute facing entity @a[tag=dv_santi,limit=1,sort=nearest] feet run tp @s ~ ~ ~ ~ 0
tag @s add dv_jtowards
execute as @a[tag=dv_santi,distance=..200] run scoreboard players add @s dv.juli 180
