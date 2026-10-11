scoreboard players set #ckey dv.dev 1
kill @e[type=item_display,tag=dv_cllave_vis]
playsound canon:cata.reja master @a[tag=dv_kpart] ~ ~ ~ 0.6 1.4
tellraw @a[tag=dv_kpart] [{"selector":"@a[tag=dv_talker]","color":"#e8c9a8"},{"text":" encontró una llave oxidada. Ahora: la reja.","color":"#9a9a9a","italic":true}]
kill @s
