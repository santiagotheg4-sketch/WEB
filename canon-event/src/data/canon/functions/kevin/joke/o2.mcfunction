scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Fui al médico y le dije que me dolía aquí, aquí y aquí. Tenía el dedo roto.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 140
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Fui al médico y le dije que me dolía aquí, aquí y aquí. Tenía el dedo roto.", "color": "white", "italic": true}]
function canon:kevin/laugh
scoreboard players set #k dv.tmp 1
