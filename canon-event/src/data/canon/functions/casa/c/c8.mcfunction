scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Ven. Sígueme... Ves, no hay nadie arriba. ¿O sí?", "color": "#ffe3ee"}',background:1342177280}
scoreboard players set @s dv.say 120
tellraw @a[distance=..10] [{"text": "Juli: ", "color": "#f2a7c3"},{"text": "Ven. Sígueme... Ves, no hay nadie arriba. ¿O sí?", "color": "white", "italic": true}]
tp @s @e[type=marker,tag=dv_jroom6,limit=1]
scoreboard players set #jroom dv.dev 6
scoreboard players set @s dv.timer2 0
playsound canon:sueno.blanco_eco ambient @a[tag=dv_jtalk] ~ ~ ~ 1 0.8
schedule function canon:casa/upstairs_scare 100t replace
