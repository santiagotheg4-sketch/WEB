scoreboard players set @s dv.state 0
tag @a[distance=..1.8,gamemode=!spectator,limit=1,sort=nearest] add dv_dcaught
execute as @a[tag=dv_dcaught] at @s run function canon:diana/jumpscare
execute as @a[distance=..12,tag=!dv_dcaught] at @s run playsound canon:diana.scream master @s ~ ~ ~ 1 0.9
execute as @a[distance=..12] run function canon:fx/shake_big
damage @a[tag=dv_dcaught,limit=1] 16 canon:diana by @s
effect give @a[tag=dv_dcaught] minecraft:wither 4 1
effect give @a[tag=dv_dcaught] minecraft:nausea 8 0
effect give @a[tag=dv_dcaught] minecraft:blindness 2 0
execute as @a[distance=..64] run function canon:diana/fed_big
tag @a remove dv_dcaught
function canon:diana/vanish
