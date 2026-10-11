scoreboard players operation #oldstage dv.dev = #stage dv.dev
scoreboard players set #stage dv.dev 0
execute if score #met dv.dev matches 1 run scoreboard players set #stage dv.dev 1
execute if score #met dv.dev matches 1 if score #sane dv.dev matches 750.. if score #love dv.dev matches 200.. run scoreboard players set #stage dv.dev 2
execute if score #met dv.dev matches 1 if score #sane dv.dev matches 550..749 run scoreboard players set #stage dv.dev 3
execute if score #met dv.dev matches 1 if score #sane dv.dev matches 350..549 run scoreboard players set #stage dv.dev 4
execute if score #met dv.dev matches 1 if score #sane dv.dev matches 150..349 run scoreboard players set #stage dv.dev 5
execute if score #met dv.dev matches 1 if score #sane dv.dev matches ..149 run scoreboard players set #stage dv.dev 6
execute unless score #stage dv.dev = #oldstage dv.dev run function canon:devota/g/stage_changed
