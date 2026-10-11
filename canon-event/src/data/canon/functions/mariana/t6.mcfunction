scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_mari_bubble,distance=..40] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":".","color":"dark_red"}',background:1879048192}
function canon:mariana/bubble
scoreboard players set #ok dv.tmp 0
execute as @a[tag=dv_talker,limit=1] at @s rotated ~ 0 positioned ^ ^ ^-1.8 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 run tp @s @e[type=marker,tag=dv_spot,limit=1]
kill @e[type=marker,tag=dv_spot]
execute at @s facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ ~
tag @s add dv_stare
tag @s remove dv_bailando
function canon:mariana/stop_music
playsound canon:fx.heartbeat_fast ambient @a[tag=dv_talker] ~ ~ ~ 1 1
