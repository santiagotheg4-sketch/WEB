scoreboard players add #love dv.dev 30
scoreboard players add #sane dv.dev 40
particle minecraft:heart ~ ~2.2 ~ 0.3 0.2 0.3 0 5 normal
playsound canon:fx.gift neutral @a[distance=..16] ~ ~ ~ 0.6 1.3
function canon:devota/expr/love
function canon:devota/clear_acts
tag @s add dv_offering
scoreboard players set @s dv.jeal 30
execute if score #es dv.tmp matches ..3 run function canon:devota/thanks_kind
execute if score #es dv.tmp matches 4.. run function canon:devota/thanks_creepy
