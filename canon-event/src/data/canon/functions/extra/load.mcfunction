scoreboard objectives add dv.kv trigger
scoreboard objectives add dv.jr trigger
scoreboard objectives add dv.mst minecraft.mined:minecraft.stone
scoreboard objectives add dv.mds minecraft.mined:minecraft.deepslate
scoreboard objectives add dv.ncd dummy
scoreboard objectives add dv.kz dummy
scoreboard objectives add dv.sb dummy
scoreboard objectives add dv.jcs dummy
scoreboard objectives add dv.mus dummy
scoreboard objectives add dv.kpcd dummy
execute unless score #miron dv.cfg matches 0.. run scoreboard players set #miron dv.cfg 1
execute unless score #kprog dv.dev matches -999999..999999 run scoreboard players set #kprog dv.dev 0
execute unless score #kdays dv.dev matches -999999..999999 run scoreboard players set #kdays dv.dev 0
execute unless score #kev dv.dev matches -999999..999999 run scoreboard players set #kev dv.dev 0
execute unless score #kt dv.dev matches -999999..999999 run scoreboard players set #kt dv.dev 0
execute unless score #kevcd dv.dev matches -999999..999999 run scoreboard players set #kevcd dv.dev 600
execute unless score #mironcd dv.dev matches -999999..999999 run scoreboard players set #mironcd dv.dev 1200
execute unless score #casa_built dv.build matches 0.. run scoreboard players set #casa_built dv.build 0
execute unless score #cata_built dv.build matches 0.. run scoreboard players set #cata_built dv.build 0
execute unless score #jroom dv.dev matches -999999..999999 run scoreboard players set #jroom dv.dev 0
scoreboard players set #6 dv.math 6
scoreboard players set #7 dv.math 7
scoreboard players set #9 dv.math 9
scoreboard players set #80 dv.math 80
scoreboard players set #140 dv.math 140
scoreboard players set #560 dv.math 560
