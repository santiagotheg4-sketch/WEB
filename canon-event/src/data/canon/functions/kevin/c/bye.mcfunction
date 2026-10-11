scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "¡Hágale pues! Nos vemos. Si ves a Mariana, no le digas que me viste.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 60
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "¡Hágale pues! Nos vemos. Si ves a Mariana, no le digas que me viste.", "color": "white", "italic": true}]
scoreboard players set #kevcd dv.dev 1200
scoreboard players set @s dv.mode 9
schedule function canon:kevin/bye_later 60t replace
