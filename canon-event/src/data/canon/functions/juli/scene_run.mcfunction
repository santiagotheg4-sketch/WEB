execute if score @s dv.timer matches 1 run function canon:juli/expr/surprised
execute if score @s dv.timer matches 1 run playsound canon:juli.encuentro master @a[distance=..40] ~ ~ ~ 1 1
execute if score @s dv.timer matches 4 run scoreboard players operation #id dv.tmp = @s dv.id
execute if score @s dv.timer matches 4 run execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"…Santi.","color":"#ffe3ee"}',background:1342177280}
execute if score @s dv.timer matches 4 run scoreboard players set @s dv.say 40
execute if score @s dv.timer matches ..109 run function canon:juli/face
execute if score @s dv.timer matches 30..90 if entity @a[tag=dv_jtgt,distance=1.5..] run function canon:juli/walk_to
execute if score @s dv.timer matches 52 run function canon:juli/expr/smile
execute if score @s dv.timer matches 52 run scoreboard players operation #id dv.tmp = @s dv.id
execute if score @s dv.timer matches 52 run execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"Te encontré.","color":"#ffe3ee"}',background:1342177280}
execute if score @s dv.timer matches 52 run scoreboard players set @s dv.say 50
execute if score @s dv.timer matches 84 run tag @s add dv_jreach
execute if score @s dv.timer matches 84 run scoreboard players operation #id dv.tmp = @s dv.id
execute if score @s dv.timer matches 84 run execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¿Vienes conmigo?","color":"#ffe3ee"}',background:1342177280}
execute if score @s dv.timer matches 84 run scoreboard players set @s dv.say 60
execute if score @s dv.timer matches 110 run tag @s remove dv_jreach
execute if score @s dv.timer matches 110 run tag @s add dv_jfloat
execute if score @s dv.timer matches 110 run effect give @a[tag=dv_jtgt] minecraft:slow_falling infinite 0 true
execute if score @s dv.timer matches 110..190 run tp @s ~ ~0.04 ~
execute if score @s dv.timer matches 110..190 as @a[tag=dv_jtgt] at @s run tp @s ~ ~0.04 ~
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=marker,tag=dv_jlook] if score @s dv.id = #id dv.tmp run tag @s add dv_jl_me
execute if score @s dv.timer matches 2.. as @a[tag=dv_jtgt] at @s run function canon:juli/scene/look
tag @e[tag=dv_jl_me] remove dv_jl_me
execute if score @s dv.timer matches 1.. if score #m2 dv.clock matches 0 run particle minecraft:cherry_leaves ~ ~1.2 ~ 1.5 1.2 1.5 0 6 normal
execute if score @s dv.timer matches 110.. if score #m4 dv.clock matches 0 run particle minecraft:end_rod ~ ~1 ~ 1.2 1.2 1.2 0.02 6 normal
execute if score @s dv.timer matches 116 at @a[tag=dv_jtgt,limit=1] run function canon:juli/fw/0
execute if score @s dv.timer matches 124 at @a[tag=dv_jtgt,limit=1] run function canon:juli/fw/1
execute if score @s dv.timer matches 134 at @a[tag=dv_jtgt,limit=1] run function canon:juli/fw/2
execute if score @s dv.timer matches 144 at @a[tag=dv_jtgt,limit=1] run function canon:juli/fw/3
execute if score @s dv.timer matches 152 at @a[tag=dv_jtgt,limit=1] run function canon:juli/fw/4
execute if score @s dv.timer matches 160 at @a[tag=dv_jtgt,limit=1] run function canon:juli/fw/5
execute if score @s dv.timer matches 166 at @a[tag=dv_jtgt,limit=1] run function canon:juli/fw/6
execute if score @s dv.timer matches 172 at @a[tag=dv_jtgt,limit=1] run function canon:juli/fw/7
execute if score @s dv.timer matches 150 run function canon:juli/expr/soft
execute if score @s dv.timer matches 150 run scoreboard players operation #id dv.tmp = @s dv.id
execute if score @s dv.timer matches 150 run execute as @e[type=text_display,tag=dv_juli_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"Quédate conmigo un rato.","color":"#ffe3ee"}',background:1342177280}
execute if score @s dv.timer matches 150 run scoreboard players set @s dv.say 60
execute if score @s dv.timer matches 176 as @a[distance=..24] run title @s times 0 30 10
execute if score @s dv.timer matches 176 as @a[distance=..24] run title @s subtitle ""
execute if score @s dv.timer matches 176 as @a[distance=..24] run title @s title ["",{"text":"","font":"canon:susto","color":"white"}]
execute if score @s dv.timer matches 186 run playsound canon:fx.whoosh_white master @a[distance=..24] ~ ~ ~ 1 1
execute if score @s dv.timer matches 190 as @a[tag=dv_jtgt] run title @s times 20 40 30
execute if score @s dv.timer matches 190 as @a[tag=dv_jtgt] run title @s subtitle ""
execute if score @s dv.timer matches 190 as @a[tag=dv_jtgt] run title @s title ["",{"text":"","font":"canon:susto","color":"white"}]
execute if score @s dv.timer matches 212 as @a[tag=dv_jtgt] run function canon:juli/scene/to_dream
execute if score @s dv.timer matches 212 run function canon:juli/vanish
