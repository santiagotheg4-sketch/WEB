scoreboard players set @s dv.state 0
playsound canon:diana.scream hostile @a[distance=..64] ~ ~ ~ 1.6 0.6
execute as @a[tag=dv_dtgt] run function canon:diana/hunt_survived
function canon:diana/vanish
