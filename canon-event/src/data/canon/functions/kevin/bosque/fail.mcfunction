execute as @e[type=zombie,tag=dv_alto] at @s run function canon:alto/vanish
stopsound @a music canon:music.bosque
execute at @e[type=marker,tag=dv_bosque_c,limit=1] at @a[distance=..140,limit=1,sort=nearest] run function canon:kevin/arrive_here
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/bosque/fail_kevin
function canon:kevin/bosque/cleanup
