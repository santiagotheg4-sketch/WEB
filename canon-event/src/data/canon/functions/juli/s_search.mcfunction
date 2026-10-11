execute if score @s dv.timer matches 1 run playsound canon:juli.theme ambient @a[distance=..48] ~ ~ ~ 0.9 1
execute if score @s dv.timer matches 1 run function canon:juli/expr/smile
execute if score #m20 dv.clock matches 0 if score @s dv.timer matches 20.. if score @s dv.say matches ..0 if predicate canon:azar/1en4 run function canon:juli/search/call
execute if score #m40 dv.clock matches 0 if predicate canon:azar/1en5 run playsound canon:juli.hum ambient @a[distance=..32] ~ ~ ~ 0.7 1
execute if score #m40 dv.clock matches 0 run title @a[tag=dv_jtgt,distance=..64] actionbar {"text":"Alguien dice tu nombre…","color":"#f2a7c3","italic":true}
execute if entity @a[tag=dv_jtgt,distance=3.5..64] run function canon:juli/walk_to
execute unless entity @a[tag=dv_jtgt,distance=3.5..] run function canon:juli/face
execute if entity @a[tag=dv_jtgt,distance=..3.5] run function canon:juli/start_scene
execute if score @s dv.state matches 2 unless entity @a[tag=dv_jtgt,distance=..64] run function canon:juli/lost
execute if score @s dv.state matches 2 if score @s dv.timer matches 2400.. run function canon:juli/lost
