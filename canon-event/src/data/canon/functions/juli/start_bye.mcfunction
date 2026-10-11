scoreboard players set @s dv.state 5
scoreboard players set @s dv.timer 0
execute unless entity @s[tag=dv_jtowards] facing entity @a[tag=dv_jtgt,limit=1] feet run tp @s ~ ~ ~ ~180 0
