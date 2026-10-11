execute as @a[tag=dv_kpart] unless entity @s[x=19998,y=-52,z=19998,dx=54,dy=12,dz=46] run tag @s remove dv_kpart
execute unless entity @a[tag=dv_kpart] run function canon:kevin/cata/fail
execute if score #kt dv.dev matches 400 in minecraft:overworld positioned 20003.5 -49 20003.5 run function canon:masa/spawn
execute if score #kt dv.dev matches 560 run playsound canon:masa.rugido hostile @a[tag=dv_kpart] ~ ~ ~ 1 0.8
execute if score #kt dv.dev matches 560 run tellraw @a[tag=dv_kpart] {"text": "Algo enorme se mueve detrás de ustedes. Respira.", "color": "#9a9a9a", "italic": true}
scoreboard players operation #c dv.tmp = #kt dv.dev
scoreboard players operation #c dv.tmp %= #560 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:cata.ambient ambient @a[tag=dv_kpart] ~ ~ ~ 1 1
execute as @a[tag=dv_kpart] at @s if predicate canon:azar/1en600 run playsound canon:cata.derrumbe ambient @s ^ ^ ^-8 0.8 1
execute if score #m40 dv.clock matches 0 as @e[type=item_display,tag=dv_cllave_vis] at @s run particle minecraft:soul ~ ~0.3 ~ 0.1 0.2 0.1 0.01 1 normal
execute as @a[tag=dv_kpart] at @s if entity @s[x=20042,y=-50,z=20037,dx=2,dy=4,dz=3] run function canon:kevin/cata/player_out
execute if score #kt dv.dev matches 12000.. run function canon:kevin/cata/fail
