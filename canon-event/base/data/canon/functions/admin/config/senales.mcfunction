execute if score #senales dv.cfg matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score #senales dv.cfg matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation #senales dv.cfg = #tg dv.tmp
function canon:admin/config
