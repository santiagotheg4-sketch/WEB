execute in minecraft:overworld run fill 20040 -49 20037 20040 -47 20039 minecraft:air
playsound canon:cata.reja master @a[tag=dv_kpart] ~ ~ ~ 1 1
tellraw @a[tag=dv_kpart] {"text": "La reja chirría y se abre. Hay una escalera al fondo. ¡Corran!", "color": "#e8c9a8", "italic": true}
kill @s
