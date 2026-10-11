summon minecraft:armor_stand ~ ~0.55 ~ {Tags:["dv_seat","dv_seat_new"],Invisible:1b,Marker:1b,NoGravity:1b,Invulnerable:1b,Silent:1b}
execute rotated as @e[type=item_display,tag=dv_mueble_sillon,distance=..0.6,limit=1,sort=nearest] as @e[type=armor_stand,tag=dv_seat_new,limit=1] positioned as @s run tp @s ~ ~ ~ ~ 0
ride @a[tag=dv_talker,limit=1] mount @e[type=armor_stand,tag=dv_seat_new,limit=1]
tag @e[type=armor_stand,tag=dv_seat_new] remove dv_seat_new
