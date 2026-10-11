execute unless entity @s[tag=dv_revived] if predicate canon:azar/1en3 run summon minecraft:marker ~ ~ ~ {Tags:["dv_revive"]}
scoreboard players set @e[type=marker,tag=dv_revive,distance=..1] dv.timer 4
