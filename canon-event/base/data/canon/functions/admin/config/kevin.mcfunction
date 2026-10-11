execute if score #kevin dv.cfg matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score #kevin dv.cfg matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation #kevin dv.cfg = #tg dv.tmp
function canon:admin/config
