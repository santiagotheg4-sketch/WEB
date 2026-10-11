scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=item_display,tag=dv_carbody] if score @s dv.id = #id dv.tmp run kill @s
tp @s ~ -250 ~
kill @s
