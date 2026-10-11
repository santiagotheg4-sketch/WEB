scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Unos billetes. Los gané en una apuesta con un vagabundo.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 90
tellraw @a[distance=..20] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Unos billetes. Los gané en una apuesta con un vagabundo.", "color": "white", "italic": true}]
loot give @a[tag=dv_ktalk] loot canon:items/billete
scoreboard players set #k dv.tmp 1
