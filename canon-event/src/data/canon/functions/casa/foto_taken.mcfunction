kill @e[type=item_display,tag=dv_cfoto_vis]
tellraw @a[tag=dv_talker] {"text":"Es una foto de Juli riéndose en un parque. Atrás alguien escribió: «no me olvides».","color":"#f2a7c3","italic":true}
loot give @a[tag=dv_talker] loot canon:items/petalo
playsound canon:juli.chime ambient @a[tag=dv_talker] ~ ~ ~ 0.8 1
execute as @e[type=zombie,tag=dv_jcasa,limit=1] at @s run function canon:casa/thanks
kill @s
