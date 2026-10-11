execute on passengers run kill @s
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[tag=dv_link] if score @s dv.id = #id dv.tmp run kill @s
data merge entity @s {DeathLootTable:"canon:vacio"}
tp @s ~ -250 ~
kill @s
