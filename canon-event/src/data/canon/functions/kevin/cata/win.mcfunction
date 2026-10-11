execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
playsound canon:cata.derrumbe master @a[tag=dv_cout] ~ ~ ~ 1 0.8
tellraw @a[tag=dv_cout] {"text": "Detrás de ustedes, el túnel se derrumba. Kevin gritaba: «¡Vayan, ya los alcanzo!»", "color": "#9a9a9a", "italic": true}
execute if score #kprog dv.dev matches ..3 run tellraw @a[tag=dv_cout] {"text": "Kevin no salió.", "color": "#c94a4a", "italic": true}
execute if score #kprog dv.dev matches 5.. run tellraw @a[tag=dv_cout] {"text": "Un rato después, Kevin sale de una alcantarilla, lleno de polvo, riéndose.", "color": "#ffb347", "italic": true}
execute if score #kprog dv.dev matches 5.. run scoreboard players set #kevcd dv.dev 30
execute if score #kprog dv.dev matches ..3 run function canon:kevin/dias/begin
tag @a remove dv_cout
function canon:kevin/cata/cleanup
