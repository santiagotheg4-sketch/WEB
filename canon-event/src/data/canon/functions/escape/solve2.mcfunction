scoreboard players set #sol2 dv.puzzle 1
execute in canon:valle_quieto run setblock -49 64 -42 minecraft:iron_door[facing=south,half=lower,hinge=left,open=true,powered=false]
execute in canon:valle_quieto run setblock -49 65 -42 minecraft:iron_door[facing=south,half=upper,hinge=left,open=true,powered=false]
execute in canon:valle_quieto run playsound minecraft:block.iron_door.open block @a -49 64 -42 1 0.9
execute in canon:valle_quieto run playsound canon:music.rocola record @a[x=-49,y=64,z=-42,distance=..20] -49 64 -42 0.5 1.2
execute in canon:valle_quieto as @a[x=-49,y=64,z=-42,distance=..20] run title @s actionbar {"text":"La caja fuerte se abre con un clic.","color":"#9fd8b0","italic":true}
