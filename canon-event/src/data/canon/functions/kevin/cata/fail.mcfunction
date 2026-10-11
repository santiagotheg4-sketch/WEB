execute as @a[x=19998,y=-52,z=19998,dx=54,dy=12,dz=46] at @s run function canon:util/tp_return
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
tellraw @a[tag=dv_kpart] {"text": "Las catacumbas los escupen afuera. Kevin quedó abajo... por ahora.", "color": "#9a9a9a", "italic": true}
scoreboard players set #kevcd dv.dev 600
function canon:kevin/cata/cleanup
