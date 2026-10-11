execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
function canon:kevin/dias/begin
tellraw @s {"text":"[Canon Event] Empiezan los 3 días sin Kevin.","color":"dark_gray"}
