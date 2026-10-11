scoreboard players set #kev dv.dev 3
scoreboard players set #kt dv.dev -100000
scoreboard players set #ckey dv.dev 0
tag @a[gamemode=!spectator,distance=..32] add dv_kpart
execute if score #cata_built dv.build matches 0 run function canon:kevin/cata/build_start
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_kbubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text": "Síganme. Y no toquen los huesos. Bueno, tóquenlos si quieren, pero después no lloren.", "color": "#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 120
tellraw @a[tag=dv_kpart] [{"text": "Kevin: ", "color": "#ffb347"},{"text": "Síganme. Y no toquen los huesos. Bueno, tóquenlos si quieren, pero después no lloren.", "color": "white", "italic": true}]
tellraw @a[tag=dv_kpart] {"text": "(Bajando a las catacumbas...)", "color": "gray", "italic": true}
schedule function canon:kevin/cata/enter_wait 40t replace
