scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^ ^ ^-8 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:nicolas/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run tellraw @s {"text": "Pasos pesados detrás de ti. Alguien se ríe bajito.", "color": "#8a8a96", "italic": true}
execute if score #ok dv.tmp matches 1 run playsound canon:nicolas.risa hostile @s ^ ^ ^-10 1 0.9
execute if score #ok dv.tmp matches 1 run playsound canon:mina.ambient ambient @s ~ ~ ~ 0.8 1
execute if score #ok dv.tmp matches 1 as @e[type=wolf,tag=dv_luna,distance=..24] at @s run function canon:luna/n/nicolas
