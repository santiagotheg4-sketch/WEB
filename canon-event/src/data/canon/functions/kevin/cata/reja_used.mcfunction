execute if score #ckey dv.dev matches 0 run tellraw @a[tag=dv_talker] {"text": "La reja está cerrada con candado. Necesitan una llave.", "color": "#9a9a9a", "italic": true}
execute if score #ckey dv.dev matches 0 run playsound canon:cata.reja master @a[tag=dv_talker] ~ ~ ~ 0.5 0.6
execute if score #ckey dv.dev matches 1 run function canon:kevin/cata/open
