execute if score #paralisis dv.cfg matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score #paralisis dv.cfg matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation #paralisis dv.cfg = #tg dv.tmp
function canon:admin/config
