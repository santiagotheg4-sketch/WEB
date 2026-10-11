scoreboard players set @s dv.mode 3
scoreboard players set @s dv.timer 0
scoreboard players set @s dv.talkcd 300
scoreboard players set #lalert dv.dev 200
function canon:luna/say_run
function canon:luna/bark3
execute as @a[distance=..24] run function canon:hud/peek
