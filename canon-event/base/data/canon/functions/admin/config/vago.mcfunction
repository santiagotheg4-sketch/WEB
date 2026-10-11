execute if score #vago dv.cfg matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score #vago dv.cfg matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation #vago dv.cfg = #tg dv.tmp
function canon:admin/config
