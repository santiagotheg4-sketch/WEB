scoreboard players set #d dv.tmp 99
execute if entity @a[tag=dv_tgt,distance=..48] run scoreboard players set #d dv.tmp 48
execute if entity @a[tag=dv_tgt,distance=..28] run scoreboard players set #d dv.tmp 28
execute if entity @a[tag=dv_tgt,distance=..16] run scoreboard players set #d dv.tmp 16
execute if entity @a[tag=dv_tgt,distance=..8] run scoreboard players set #d dv.tmp 8
execute if entity @a[tag=dv_tgt,distance=..5] run scoreboard players set #d dv.tmp 5
execute if entity @a[tag=dv_tgt,distance=..2.3] run scoreboard players set #d dv.tmp 2
scoreboard players set #seen dv.tmp 0
execute if entity @a[distance=..48,scores={dv.seen=1..}] run scoreboard players set #seen dv.tmp 1
scoreboard players set #heard dv.tmp 0
execute if entity @a[distance=..4,scores={dv.noise=1..}] run scoreboard players set #heard dv.tmp 1
execute if entity @a[distance=..14,scores={dv.noise=2..}] run scoreboard players set #heard dv.tmp 1
execute if entity @a[distance=..24,scores={dv.noise=3..}] run scoreboard players set #heard dv.tmp 1
execute if entity @a[distance=..36,scores={dv.noise=4..}] run scoreboard players set #heard dv.tmp 1
execute if entity @a[distance=..64,scores={dv.noise=5..}] run scoreboard players set #heard dv.tmp 1
execute if score #apagon dv.ev matches 1.. if entity @a[distance=..22,scores={dv.noise=2..}] run scoreboard players set #heard dv.tmp 1
execute if entity @a[distance=..64,scores={dv.sleep=1..}] if entity @a[distance=..64,scores={dv.noise=..1}] run scoreboard players set #heard dv.tmp 0
