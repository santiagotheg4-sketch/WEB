effect give @s minecraft:darkness 4 0 true
playsound canon:fx.blackout ambient @s ~ ~ ~ 0.7 1
tellraw @s {"text": "Las luces del pueblo parpadean y se apagan un segundo.", "color": "gray", "italic": true}
scoreboard players set #k dv.tmp 1
