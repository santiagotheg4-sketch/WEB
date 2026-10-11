execute as @e[type=zombie,tag=dv_alto] at @s run function canon:alto/vanish
stopsound @a[tag=dv_kpart] music canon:music.bosque
effect clear @a[tag=dv_kpart] minecraft:darkness
execute at @a[tag=dv_talker,limit=1] run function canon:kevin/arrive_here
execute if score #kprog dv.dev matches ..2 run scoreboard players set #kprog dv.dev 3
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/bosque/win_kevin
function canon:kevin/bosque/cleanup
