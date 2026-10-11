# como jugador: susto con imagen (si los sustos están activos)
execute if score #susto dv.cfg matches 1 run title @s times 0 9 7
execute if score #susto dv.cfg matches 1 run title @s subtitle ""
execute if score #susto dv.cfg matches 1 run title @s title ["",{"text":"\ue100","font":"canon:susto","color":"white"}]
function canon:fx/shake_big
