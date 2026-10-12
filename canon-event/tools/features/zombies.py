"""Zombies inteligentes (solo zombies normales: type=zombie sin dv_brain).

- OÍDO: si haces ruido (dv.noise del mod base: caminar, correr, saltar, disparar) los zombies
  cercanos caminan hacia donde lo hiciste. Truco: un aldeano señuelo invisible e invulnerable,
  enterrado bajo tus pies unos segundos (los zombies persiguen aldeanos sin necesidad de verlos).
  Agachado no hace ruido.
- LLAMADA: el zombie gritón (y a veces cualquiera) que te tiene cerca llama a la horda.
- ESCALAR: si estás encima de ellos, ponen tierra bajo sus pies y suben.
- ROMPER: si están atascados frente a un bloque débil, lo rompen tras unos segundos.
- VARIANTES: corredor, tanque, gritón, minero (en cuevas). De noche son más rápidos.
- LUNA DE SANGRE (evento canónico 1): más zombies, más fuertes, cielo rojo.
"""
from canon.shim import *  # noqa: F401,F403
from canon import shim

Z = '@e[type=zombie,tag=!dv_brain'


def build(c):
    shim.use(c)
    c.config('zomb_listos', 'Zombies inteligentes (oído, horda, escalar)', 1)
    c.config('zomb_rompen', 'Zombies rompen bloques débiles', 0)
    for o in ('dv.zx', 'dv.zz', 'dv.zst', 'dv.zpil', 'dv.zlure', 'dv.zcall'):
        c.objective(o)
    for n in (10, 20, 40):
        c.const(n)
    c.json('data/canon/tags/blocks/zomb_rompible.json', {'values': [
        'minecraft:dirt', 'minecraft:grass_block', 'minecraft:coarse_dirt', 'minecraft:sand', 'minecraft:gravel', 'minecraft:glass',
        'minecraft:glass_pane', '#minecraft:leaves', '#minecraft:wool', 'minecraft:hay_block', 'minecraft:cobweb', 'minecraft:snow_block',
        'minecraft:white_stained_glass', 'minecraft:tinted_glass', 'minecraft:mud', 'minecraft:clay', 'minecraft:farmland',
        'minecraft:dirt_path', 'minecraft:moss_block', 'minecraft:melon', 'minecraft:pumpkin']})
    c.on('tick', f'''
execute if score #zomb_listos dv.cfg matches 1 if score #m10 dv.clock matches 3 run function canon:zomb/ciclo
''')
    c.on('second', '''
execute if score #zomb_listos dv.cfg matches 1 as @a[gamemode=!spectator,gamemode=!creative] at @s run function canon:zomb/oido
execute as @e[type=villager,tag=dv_zlure] run function canon:zomb/lure_vida
execute if score #canon_ev dv.dev matches 1 run function canon:zomb/sangre/second
execute unless score #canon_ev dv.dev matches 1 run scoreboard players set #zs_ann dv.dev 0
''')
    # -------------------------------------------------------- ciclo (cada 10 ticks)
    F('zomb/ciclo', f'''
tag @e[type=zombie,tag=dv_zdone] remove dv_zdone
execute as @a[gamemode=!spectator] at @s as {Z},tag=!dv_zdone,distance=..40] at @s run function canon:zomb/z
''')
    F('zomb/z', f'''
tag @s add dv_zdone
execute unless entity @s[tag=dv_zinit] run function canon:zomb/init
execute if entity @s[tag=dv_zgriton] if entity @a[gamemode=!spectator,gamemode=!creative,distance=..12] unless score @s dv.zcall matches 1.. run function canon:zomb/llamar
execute if entity @s[tag=!dv_zgriton] if entity @a[gamemode=!spectator,gamemode=!creative,distance=..8] unless score @s dv.zcall matches 1.. if predicate canon:azar/1en40 run function canon:zomb/llamar
scoreboard players remove @s[scores={{dv.zcall=1..}}] dv.zcall 1
execute positioned ~-2.5 ~2.6 ~-2.5 if entity @a[gamemode=!spectator,gamemode=!creative,dx=4,dy=10,dz=4] positioned ~2.5 ~-2.6 ~2.5 unless score @s dv.zpil matches 6.. run function canon:zomb/escalar
execute if score #zomb_rompen dv.cfg matches 1 if entity @a[gamemode=!spectator,gamemode=!creative,distance=..14] run function canon:zomb/atasco
execute if entity @s[tag=dv_zminero] if entity @a[gamemode=!spectator,gamemode=!creative,distance=..14] run function canon:zomb/atasco_minero
''')
    F('zomb/init', '''
tag @s add dv_zinit
data merge entity @s {CanBreakDoors:1b,CanPickUpLoot:1b}
attribute @s minecraft:generic.follow_range base set 40
scoreboard players set @s dv.zpil 0
scoreboard players set @s dv.zst 0
execute if predicate canon:de_noche run attribute @s minecraft:generic.movement_speed base set 0.26
execute if predicate canon:azar/1en8 run function canon:zomb/v/corredor
execute unless entity @s[tag=dv_zvar] if predicate canon:azar/1en10 run function canon:zomb/v/tanque
execute unless entity @s[tag=dv_zvar] if predicate canon:azar/1en8 run function canon:zomb/v/griton
execute unless entity @s[tag=dv_zvar] if entity @s[y=-64,dy=104] if predicate canon:azar/1en5 run function canon:zomb/v/minero
execute unless entity @s[tag=dv_zvar] if predicate canon:azar/1en12 run function canon:zomb/v/muerto
''')
    F('zomb/v/corredor', '''
tag @s add dv_zvar
tag @s add dv_zcorredor
attribute @s minecraft:generic.movement_speed base set 0.34
data merge entity @s {CustomName:'{"text":"Zombi corredor","color":"#c94a4a"}',ArmorItems:[{},{},{},{id:"minecraft:leather_helmet",Count:1b,tag:{display:{color:9109504}}}],ArmorDropChances:[0f,0f,0f,0f]}
''')
    F('zomb/v/tanque', '''
tag @s add dv_zvar
tag @s add dv_ztanque
attribute @s minecraft:generic.max_health base set 50
attribute @s minecraft:generic.movement_speed base set 0.18
attribute @s minecraft:generic.attack_damage base set 7
attribute @s minecraft:generic.knockback_resistance base set 0.8
data merge entity @s {Health:50f,CustomName:'{"text":"Zombi tanque","color":"#8a8a8a"}',ArmorItems:[{id:"minecraft:iron_boots",Count:1b},{id:"minecraft:iron_leggings",Count:1b},{id:"minecraft:iron_chestplate",Count:1b},{id:"minecraft:iron_helmet",Count:1b}],ArmorDropChances:[0.05f,0.05f,0.05f,0.05f]}
''')
    F('zomb/v/griton', '''
tag @s add dv_zvar
tag @s add dv_zgriton
data merge entity @s {CustomName:'{"text":"Zombi gritón","color":"#d9a441"}'}
''')
    F('zomb/v/minero', '''
tag @s add dv_zvar
tag @s add dv_zminero
data merge entity @s {CustomName:'{"text":"Zombi minero","color":"#b08a5a"}',HandItems:[{id:"minecraft:iron_pickaxe",Count:1b},{}],HandDropChances:[0.08f,0f],ArmorItems:[{},{},{},{id:"minecraft:golden_helmet",Count:1b}],ArmorDropChances:[0f,0f,0f,0f]}
''')
    F('zomb/v/muerto', '''
tag @s add dv_zvar
tag @s add dv_zmuerto
data merge entity @s {NoAI:1b,Silent:1b}
''')
    # el que se hace el muerto: se levanta cuando te acercas
    c.on('second', f'execute as @a[gamemode=!spectator,gamemode=!creative] at @s as {Z},tag=dv_zmuerto,distance=..4] at @s run function canon:zomb/levantarse')
    F('zomb/levantarse', '''
tag @s remove dv_zmuerto
data merge entity @s {NoAI:0b,Silent:0b}
playsound minecraft:entity.zombie.ambient hostile @a[distance=..16] ~ ~ ~ 1.4 0.7
effect give @s minecraft:speed 4 1 true
''')
    # -------------------------------------------------------- oído: señuelo en la posición del ruido
    F('zomb/oido', '''
scoreboard players set #zr dv.tmp 0
execute if score @s dv.noise matches 2 run scoreboard players set #zr dv.tmp 1
execute if score @s dv.noise matches 3..4 run scoreboard players set #zr dv.tmp 2
execute if score @s dv.noise matches 5.. run scoreboard players set #zr dv.tmp 3
execute if score #zr dv.tmp matches 1 if entity @e[type=zombie,tag=!dv_brain,distance=6..14] run function canon:zomb/senuelo
execute if score #zr dv.tmp matches 2 if entity @e[type=zombie,tag=!dv_brain,distance=6..24] run function canon:zomb/senuelo
execute if score #zr dv.tmp matches 3 if entity @e[type=zombie,tag=!dv_brain,distance=6..48] run function canon:zomb/senuelo
''')
    F('zomb/senuelo', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #zf dv.tmp 0
execute as @e[type=villager,tag=dv_zlure] if score @s dv.pid = #pid dv.tmp run function canon:zomb/lure_mover
execute if score #zf dv.tmp matches 0 positioned ~ ~-1.6 ~ run function canon:zomb/lure_nuevo
''')
    F('zomb/lure_mover', 'tp @s ~ ~-1.6 ~\nscoreboard players set @s dv.zlure 5\nscoreboard players set #zf dv.tmp 1')
    F('zomb/lure_nuevo', '''
summon minecraft:villager ~ ~ ~ {Tags:["dv_zlure","dv_zlure_new"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:0b,NoGravity:1b,VillagerData:{profession:"minecraft:nitwit",level:1,type:"minecraft:plains"}}
effect give @e[type=villager,tag=dv_zlure_new] minecraft:invisibility infinite 0 true
scoreboard players operation @e[type=villager,tag=dv_zlure_new] dv.pid = #pid dv.tmp
scoreboard players set @e[type=villager,tag=dv_zlure_new] dv.zlure 5
tag @e[type=villager,tag=dv_zlure_new] remove dv_zlure_new
''')
    F('zomb/lure_vida', '''
scoreboard players remove @s dv.zlure 1
execute if score @s dv.zlure matches ..0 run tp @s ~ -300 ~
execute if score @s dv.zlure matches ..0 run kill @s
''')
    # -------------------------------------------------------- llamada de horda
    F('zomb/llamar', '''
scoreboard players set @s dv.zcall 30
playsound minecraft:entity.zombie.ambient hostile @a[distance=..48] ~ ~ ~ 2 0.55
playsound minecraft:entity.zombie_villager.ambient hostile @a[distance=..48] ~ ~ ~ 1.5 0.5
particle minecraft:angry_villager ~ ~2.2 ~ 0.3 0.2 0.3 0 3 normal
effect give @e[type=zombie,tag=!dv_brain,distance=..24] minecraft:speed 6 0 true
execute as @a[gamemode=!spectator,gamemode=!creative,distance=..16,limit=1,sort=nearest] at @s run function canon:zomb/senuelo
''')
    # -------------------------------------------------------- escalar
    F('zomb/escalar', '''
execute unless block ~ ~-0.5 ~ #canon:pasable if block ~ ~2 ~ #canon:pasable if block ~ ~ ~ #canon:pasable run function canon:zomb/escalar_ya
''')
    F('zomb/escalar_ya', '''
tp @s ~ ~1.05 ~
setblock ~ ~ ~ minecraft:dirt keep
scoreboard players add @s dv.zpil 1
playsound minecraft:block.gravel.place hostile @a[distance=..16] ~ ~ ~ 0.8 0.9
''')
    # -------------------------------------------------------- atasco: romper bloque débil hacia el jugador
    F('zomb/atasco', '''
execute store result score #zx dv.tmp run data get entity @s Pos[0] 10
execute store result score #zz dv.tmp run data get entity @s Pos[2] 10
scoreboard players operation #dx dv.tmp = #zx dv.tmp
scoreboard players operation #dx dv.tmp -= @s dv.zx
scoreboard players operation #dz dv.tmp = #zz dv.tmp
scoreboard players operation #dz dv.tmp -= @s dv.zz
scoreboard players operation @s dv.zx = #zx dv.tmp
scoreboard players operation @s dv.zz = #zz dv.tmp
scoreboard players set #quieto dv.tmp 0
execute if score #dx dv.tmp matches -2..2 if score #dz dv.tmp matches -2..2 run scoreboard players set #quieto dv.tmp 1
execute if score #quieto dv.tmp matches 0 run scoreboard players set @s dv.zst 0
execute if score #quieto dv.tmp matches 1 run function canon:zomb/golpear
''')
    F('zomb/golpear', '''
scoreboard players set #zhit dv.tmp 0
execute facing entity @a[gamemode=!spectator,gamemode=!creative,distance=..14,limit=1,sort=nearest] feet rotated ~ 0 positioned ^ ^ ^1 if block ~ ~ ~ #canon:zomb_rompible run scoreboard players set #zhit dv.tmp 1
execute facing entity @a[gamemode=!spectator,gamemode=!creative,distance=..14,limit=1,sort=nearest] feet rotated ~ 0 positioned ^ ^1 ^1 if block ~ ~ ~ #canon:zomb_rompible run scoreboard players set #zhit dv.tmp 1
execute if score #zhit dv.tmp matches 0 run scoreboard players set @s dv.zst 0
execute if score #zhit dv.tmp matches 1 run scoreboard players add @s dv.zst 1
execute if score #zhit dv.tmp matches 1 run playsound minecraft:entity.zombie.attack_wooden_door hostile @a[distance=..20] ~ ~ ~ 0.7 1.2
execute if score #zhit dv.tmp matches 1 facing entity @a[gamemode=!spectator,gamemode=!creative,distance=..14,limit=1,sort=nearest] feet rotated ~ 0 positioned ^ ^0.5 ^1 run particle minecraft:crit ~ ~ ~ 0.3 0.4 0.3 0 6 normal
execute if score @s dv.zst matches 8.. facing entity @a[gamemode=!spectator,gamemode=!creative,distance=..14,limit=1,sort=nearest] feet rotated ~ 0 run function canon:zomb/romper
''')
    F('zomb/romper', '''
scoreboard players set @s dv.zst 0
execute positioned ^ ^ ^1 if block ~ ~ ~ #canon:zomb_rompible run setblock ~ ~ ~ minecraft:air destroy
execute positioned ^ ^1 ^1 if block ~ ~ ~ #canon:zomb_rompible run setblock ~ ~ ~ minecraft:air destroy
playsound minecraft:entity.zombie.break_wooden_door hostile @a[distance=..24] ~ ~ ~ 0.8 1.3
''')
    F('zomb/atasco_minero', '''
execute if score @s dv.zst matches 6.. facing entity @a[gamemode=!spectator,gamemode=!creative,distance=..14,limit=1,sort=nearest] feet rotated ~ 0 positioned ^ ^ ^1 if block ~ ~ ~ #minecraft:base_stone_overworld run setblock ~ ~ ~ minecraft:air destroy
execute if score @s dv.zst matches 6.. facing entity @a[gamemode=!spectator,gamemode=!creative,distance=..14,limit=1,sort=nearest] feet rotated ~ 0 positioned ^ ^1 ^1 if block ~ ~ ~ #minecraft:base_stone_overworld run setblock ~ ~ ~ minecraft:air destroy
''')
    # -------------------------------------------------------- luna de sangre (evento canónico 1)
    F('zomb/sangre/second', f'''
execute if predicate canon:de_noche unless score #zs_ann dv.dev matches 1 run function canon:zomb/sangre/anuncio
execute if predicate canon:de_noche as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s run particle minecraft:dust 0.7 0 0 3 ~ ~25 ~ 20 3 20 0 30 force @s
execute if predicate canon:de_noche if score #m200 dv.clock matches 0..19 as @a[gamemode=!spectator,gamemode=!creative,predicate=canon:en_superficie,limit=1,sort=random] at @s run function canon:zomb/sangre/horda
execute if predicate canon:de_noche as {Z},tag=!dv_zsangre] run function canon:zomb/sangre/potenciar
''')
    F('zomb/sangre/anuncio', '''
scoreboard players set #zs_ann dv.dev 1
title @a times 10 60 20
title @a subtitle {"text":"Los muertos tienen hambre esta noche.","color":"#c94a4a","italic":true}
title @a title {"text":"LUNA DE SANGRE","color":"#8b0000","bold":true}
playsound minecraft:entity.wither.spawn master @a ~ ~ ~ 0.5 0.6
''')
    F('zomb/sangre/horda', '''
execute store result score #zn dv.tmp if entity @e[type=zombie,tag=!dv_brain,distance=..48]
execute if score #zn dv.tmp matches ..14 positioned ^ ^ ^-18 run function canon:zomb/sangre/uno
execute if score #zn dv.tmp matches ..14 positioned ^14 ^ ^-8 run function canon:zomb/sangre/uno
''')
    F('zomb/sangre/uno', '''
scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run summon minecraft:zombie ~ ~ ~ {Tags:["dv_zsangre_new"]}
kill @e[type=marker,tag=dv_spot]
''')
    F('zomb/sangre/potenciar', '''
tag @s add dv_zsangre
effect give @s minecraft:strength infinite 0 true
effect give @s minecraft:speed infinite 0 true
attribute @s minecraft:generic.follow_range base set 56
''')
    F('admin/zomb/variantes', '''
summon minecraft:zombie ^ ^ ^4
summon minecraft:zombie ^2 ^ ^5
summon minecraft:zombie ^-2 ^ ^5
summon minecraft:zombie ^ ^ ^7
tellraw @s {"text":"[Canon Event] 4 zombies: al acercarte (cada 10 ticks) eligen variante y empiezan a escuchar.","color":"dark_gray"}
''')
    F('admin/zomb/sangre', 'scoreboard players set #canon_ev dv.dev 1\nscoreboard players set #canon_t dv.dev 0\ntime set night')
    c.admin('/function canon:admin/zomb/variantes', 'Invocar zombies (variantes al azar)')
    c.admin('/function canon:admin/zomb/sangre', 'Forzar la Luna de sangre')
