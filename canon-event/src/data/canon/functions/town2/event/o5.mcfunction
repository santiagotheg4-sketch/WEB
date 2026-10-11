execute if score #nicolas dv.cfg matches 1 run playsound canon:nicolas.risa ambient @s ^-10 ^2 ^8 0.7 1
execute if score #nicolas dv.cfg matches 1 run tellraw @s {"text": "Una risa sale de una casa cerrada.", "color": "gray", "italic": true}
scoreboard players set #k dv.tmp 1
