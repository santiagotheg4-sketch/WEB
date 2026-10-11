playsound canon:devota.scream hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
playsound canon:fx.music_box_end ambient @a[distance=..48] ~ ~ ~ 0.8 1
scoreboard players set #cd dv.dev 1200
scoreboard players add #sane dv.dev 250
scoreboard players remove #love dv.dev 150
tellraw @a[distance=..64] {"text":"La derribaron. La oyes llorar en algún lugar. Va a volver, más tranquila… por un tiempo.","color":"#d77a8a","italic":true}
