execute if score #hud dv.cfg matches 1 run scoreboard players set #tg dv.tmp 0
execute unless score #hud dv.cfg matches 1 run scoreboard players set #tg dv.tmp 1
scoreboard players operation #hud dv.cfg = #tg dv.tmp
function canon:admin/config
