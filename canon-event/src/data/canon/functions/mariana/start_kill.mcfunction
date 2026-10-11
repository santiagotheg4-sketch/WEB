scoreboard players set @s dv.state 3
scoreboard players set @s dv.timer2 600
tag @s add dv_stare
tag @s remove dv_bailando
function canon:mariana/stop_music
function canon:mariana/bubble_clear
data merge entity @s {NoAI:0b}
attribute @s minecraft:generic.follow_range base set 64
playsound canon:fx.sub_hit ambient @a[distance=..32] ~ ~ ~ 1 0.8
title @a[distance=..20] times 0 30 10
title @a[distance=..20] subtitle {"text":"Hablaste demasiado.","color":"dark_red","italic":true}
title @a[distance=..20] title {"text":" "}
