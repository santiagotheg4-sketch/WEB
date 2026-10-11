scoreboard players set #sol1 dv.puzzle 1
execute in canon:valle_quieto run setblock -2 58 -37 minecraft:iron_door[facing=east,half=lower,hinge=left,open=true,powered=false]
execute in canon:valle_quieto run setblock -2 59 -37 minecraft:iron_door[facing=east,half=upper,hinge=left,open=true,powered=false]
execute in canon:valle_quieto run playsound minecraft:block.iron_door.open block @a -2 58 -37 1 0.7
execute in canon:valle_quieto run playsound canon:fx.gift block @a -2 58 -37 1 0.8
execute in canon:valle_quieto as @a[x=-2,y=58,z=-37,distance=..20] run title @s actionbar {"text":"Se oye un cerrojo abrirse.","color":"#9fd8b0","italic":true}
