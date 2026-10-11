scoreboard players set #lr dv.tmp 999
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a if score @s dv.pid = #tgt dv.tmp run tag @s add dv_dtgt
execute if score @s dv.state matches 4 run tag @s add dv_nolight
execute unless entity @s[tag=dv_nolight] if score @s dv.state matches 3 run function canon:diana/repelled
execute unless entity @s[tag=dv_nolight] if score @s dv.state matches 1..2 run function canon:diana/repelled_soft
execute unless entity @s[tag=dv_nolight] if score @s dv.state matches 5..7 run function canon:diana/repelled_soft
tag @s remove dv_nolight
tag @a[tag=dv_dtgt] remove dv_dtgt
