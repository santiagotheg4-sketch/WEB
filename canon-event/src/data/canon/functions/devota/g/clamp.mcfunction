execute unless score #sane dv.dev matches -999999..999999 run scoreboard players set #sane dv.dev 1000
execute unless score #love dv.dev matches -999999..999999 run scoreboard players set #love dv.dev 0
execute if score #sane dv.dev matches 1001.. run scoreboard players set #sane dv.dev 1000
execute if score #sane dv.dev matches ..-1 run scoreboard players set #sane dv.dev 0
execute if score #love dv.dev matches 1001.. run scoreboard players set #love dv.dev 1000
execute if score #love dv.dev matches ..-1 run scoreboard players set #love dv.dev 0
