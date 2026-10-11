scoreboard players set @s dv.state 0
playsound canon:diana.crack hostile @a[distance=..16] ~ ~ ~ 0.8 1.4
execute as @a[tag=dv_dtgt] run scoreboard players remove @s dv.dia 30
function canon:diana/vanish
