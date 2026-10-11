scoreboard players set @s dv.mode 0
tag @s remove dv_kdance
execute if score #kdrunk dv.dev matches 1 run function canon:kevin/fiesta/end_drunk
execute if score #kdrunk dv.dev matches 0 run function canon:kevin/fiesta/end_sober
function canon:kevin/laugh
tellraw @a[distance=..40] {"text": "(Kevin tiene otra idea. Háblale: ¿Qué hacemos hoy?)", "color": "gray", "italic": true}
