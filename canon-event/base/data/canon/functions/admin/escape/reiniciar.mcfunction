execute as @e[type=horse,tag=dv_car_town] at @s run function canon:car/remove
function canon:escape/randomize
tellraw @s {"text":"[Canon Event] El escape se reiniciará cuando el pueblo esté cargado.","color":"dark_gray"}
