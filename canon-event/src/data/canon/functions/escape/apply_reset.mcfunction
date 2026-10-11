scoreboard players set #rs_pending dv.puzzle 0
execute in canon:valle_quieto run setblock -2 58 -37 minecraft:iron_door[facing=east,half=lower,hinge=left,open=false,powered=false]
execute in canon:valle_quieto run setblock -2 59 -37 minecraft:iron_door[facing=east,half=upper,hinge=left,open=false,powered=false]
execute in canon:valle_quieto run setblock -49 64 -42 minecraft:iron_door[facing=south,half=lower,hinge=left,open=false,powered=false]
execute in canon:valle_quieto run setblock -49 65 -42 minecraft:iron_door[facing=south,half=upper,hinge=left,open=false,powered=false]
execute in canon:valle_quieto run setblock 40 64 -90 minecraft:iron_door[facing=north,half=lower,hinge=left,open=false,powered=false]
execute in canon:valle_quieto run setblock 40 65 -90 minecraft:iron_door[facing=north,half=upper,hinge=left,open=false,powered=false]
execute in canon:valle_quieto run setblock -40 64 -87 minecraft:bamboo_mosaic
execute in canon:valle_quieto run setblock -40 65 -87 minecraft:bamboo_mosaic
execute in canon:valle_quieto run setblock -41 64 -87 minecraft:bamboo_mosaic
execute in canon:valle_quieto run setblock -41 65 -87 minecraft:bamboo_mosaic
execute in canon:valle_quieto if block 6 59 -34 minecraft:lever[powered=true] run setblock 6 59 -34 minecraft:air
execute in canon:valle_quieto if block 4 59 -34 minecraft:lever[powered=true] run setblock 4 59 -34 minecraft:air
execute in canon:valle_quieto if block 2 59 -34 minecraft:lever[powered=true] run setblock 2 59 -34 minecraft:air
execute in canon:valle_quieto if block 0 59 -34 minecraft:lever[powered=true] run setblock 0 59 -34 minecraft:air
function canon:escape/levers_restore
