execute unless score @s dv.talkcd matches 1.. run scoreboard players add #love dv.dev 8
execute unless score @s dv.talkcd matches 1.. run scoreboard players add #sane dv.dev 4
scoreboard players set @s dv.talkcd 10
function canon:devota/talk_line
scoreboard players set @s dv.idle 160
execute if score @s dv.mode matches 2 run function canon:devota/watch_clicked
