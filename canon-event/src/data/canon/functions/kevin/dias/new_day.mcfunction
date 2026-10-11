scoreboard players operation #kday_last dv.dev = #kday dv.tmp
scoreboard players add #kdays dv.dev 1
execute if score #kdays dv.dev matches 2 run tellraw @a {"text": "Día 2 sin Kevin. Su celular suena apagado. De noche alguien grita tu nombre con su voz.", "color": "#ffb347", "italic": true}
execute if score #kdays dv.dev matches 3 run tellraw @a {"text": "Día 3. Encuentras una gorra negra en la puerta, mojada de barro. Esta noche no salgas.", "color": "#ffb347", "italic": true}
execute if score #kdays dv.dev matches 4.. run function canon:kevin/dias/return
