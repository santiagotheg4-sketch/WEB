clear @a[tag=dv_talker,limit=1] minecraft:paper{canon:{id:"fusible"}} 1
scoreboard players set #sol3 dv.puzzle 1
execute in canon:valle_quieto run setblock 40 64 -90 minecraft:iron_door[facing=north,half=lower,hinge=left,open=true,powered=false]
execute in canon:valle_quieto run setblock 40 65 -90 minecraft:iron_door[facing=north,half=upper,hinge=left,open=true,powered=false]
execute at @s run playsound minecraft:block.beacon.power_select block @a ~ ~ ~ 1 1.4
execute at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.3 0.3 0.1 20 normal
tellraw @a[tag=dv_talker] {"text":"Vuelve la corriente. La puerta del almacén se abre.","color":"#9fd8b0","italic":true}
