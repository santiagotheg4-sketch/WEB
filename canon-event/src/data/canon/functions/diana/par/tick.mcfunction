scoreboard players add @s dv.par 1
scoreboard players operation #pid dv.tmp = @s dv.pid
execute as @e[type=marker,tag=dv_panchor] if score @s dv.target = #pid dv.tmp run tag @s add dv_pa_me
execute as @e[type=marker,tag=dv_dlook] if score @s dv.target = #pid dv.tmp run tag @s add dv_dl_me
execute at @e[type=marker,tag=dv_pa_me,limit=1] if entity @e[type=marker,tag=dv_dl_me] run tp @s ~ ~ ~ facing entity @e[type=marker,tag=dv_dl_me,limit=1] feet
execute unless entity @e[type=marker,tag=dv_dl_me] if score @s dv.par matches 6.. run function canon:diana/par/release
tag @e[tag=dv_pa_me] remove dv_pa_me
tag @e[tag=dv_dl_me] remove dv_dl_me
execute if score @s dv.par matches 420.. run function canon:diana/par/release
