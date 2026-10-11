scoreboard players set @s dv.mode 3
scoreboard players set @s dv.timer 0
scoreboard players set @s dv.talkcd 600
scoreboard players set #lalert dv.dev 160
function canon:luna/say_watch
function canon:luna/bark2
execute as @a[distance=..24] run function canon:hud/peek
