"""Terror 4.0: linterna real, salidas de los sueños, cámara de Diana, medidor de miedo, oscuridad,
acoso en tu casa (ventanas, puerta, techo), acecho (Diana siempre por ahí, Nicolás en cuevas),
zombies tipo Resident Evil (te oyen cuando te lastiman, tocan tu puerta, se quedan mirando) y arañas que acechan.
"""
from canon.shim import *  # noqa: F401,F403
from canon import shim

# modelos que usan los que se asoman (cuerpo, cabeza, escala)
PEEK = {
    'zunga': (7320078, 7320088, 1.06),
    'miron': (7320142, None, 1.3),
    'nicolas': (7320126, 7320132, 1.0),
    'nicolas2': (7320126, 7320130, 1.0),
    'mariana': (7321000, 7321007, 1.0),
    'abuela': (7321010, 7321016, 1.0),
    'dhumana': (7320500, 7320506, 1.0),
}


def build(c):
    shim.use(c)
    c.config('miedo', 'Medidor de miedo, oscuridad y alucinaciones', 1)
    c.config('acoso', 'Acoso en tu casa y acecho', 1)
    for o in ('dv.miedo', 'dv.oscu', 'dv.home', 'dv.hcd', 'dv.luz', 'dv.ltl', 'dv.vidap', 'dv.zkn', 'dv.zmira', 'dv.acd'):
        c.objective(o)
    c.objective('dv.vida', 'health')
    for n in (2, 3, 4, 8, 10, 20, 40, 60):
        c.const(n)
    # ------------------------------------------------------------------ tags y predicados
    c.json('data/canon/tags/blocks/luz_pasa.json', {'values': ['minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:light']})
    panes = ['minecraft:glass_pane'] + [f'minecraft:{col}_stained_glass_pane' for col in (
        'white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown',
        'green', 'red', 'black')]
    c.json('data/canon/tags/blocks/vidrio.json', {'values': ['#minecraft:impermeable'] + panes})
    c.json('data/canon/predicates/muy_oscuro.json', {'condition': 'minecraft:location_check', 'predicate': {'light': {'light': {'max': 2}}}})
    luz_items = ['minecraft:torch', 'minecraft:soul_torch', 'minecraft:lantern', 'minecraft:soul_lantern', 'minecraft:glowstone',
                 'minecraft:shroomlight', 'minecraft:sea_lantern', 'minecraft:redstone_torch', 'minecraft:jack_o_lantern']
    c.json('data/canon/predicates/con_luz.json', {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'mainhand': {'items': luz_items}}}},
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'offhand': {'items': luz_items}}}},
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'effects': {'minecraft:night_vision': {}}}}]})

    # ================================================================== LINTERNA (luz real)
    c.patch('items/linterna/active', lambda s: s if 'luz/tick' in s else
            '\n'.join(l for l in s.split('\n') if 'night_vision' not in l).rstrip('\n') + '\nfunction canon:luz/tick\n')
    c.patch('items/linterna/off', lambda s: s if 'luz/apagar' in s else s.rstrip('\n') + '\nfunction canon:luz/apagar\n')
    c.patch('items/linterna/tick', lambda s: s if 'luz/apagar' in s else
            s.rstrip('\n') + '\nexecute unless predicate canon:mano/linterna if score @s dv.luz matches 1 run function canon:luz/apagar\n')
    c.on('tick', 'execute as @e[type=marker,tag=dv_luzmk] at @s run function canon:luz/ttl')
    F('luz/tick', '''
scoreboard players set #lz dv.tmp 0
execute anchored eyes positioned ^ ^ ^0.6 run function canon:luz/rayo
''')
    F('luz/rayo', '''
scoreboard players add #lz dv.tmp 1
execute if score #lz dv.tmp matches 44.. run function canon:luz/poner
execute if score #lz dv.tmp matches ..43 unless block ^ ^ ^0.5 #canon:luz_pasa run function canon:luz/poner
execute if score #lz dv.tmp matches ..43 if block ^ ^ ^0.5 #canon:luz_pasa positioned ^ ^ ^0.5 run function canon:luz/rayo
''')
    F('luz/poner', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #lf dv.tmp 0
execute align xyz positioned ~0.5 ~0.5 ~0.5 as @e[type=marker,tag=dv_luzmk] if score @s dv.pid = #pid dv.tmp run function canon:luz/mover
execute if score #lf dv.tmp matches 0 align xyz positioned ~0.5 ~0.5 ~0.5 run function canon:luz/nuevo
scoreboard players set @s dv.luz 1
''')
    F('luz/mover', '''
scoreboard players set #lf dv.tmp 1
scoreboard players set @s dv.ltl 4
execute unless entity @s[distance=..0.3] at @s if block ~ ~ ~ minecraft:light run setblock ~ ~ ~ minecraft:air
execute unless entity @s[distance=..0.3] run tp @s ~ ~ ~
execute at @s run setblock ~ ~ ~ minecraft:light[level=15] keep
''')
    F('luz/nuevo', '''
summon minecraft:marker ~ ~ ~ {Tags:["dv_luzmk","dv_luz_new"]}
scoreboard players operation @e[type=marker,tag=dv_luz_new] dv.pid = #pid dv.tmp
scoreboard players set @e[type=marker,tag=dv_luz_new] dv.ltl 4
tag @e[type=marker,tag=dv_luz_new] remove dv_luz_new
setblock ~ ~ ~ minecraft:light[level=15] keep
''')
    F('luz/ttl', '''
scoreboard players remove @s dv.ltl 1
execute if score @s dv.ltl matches ..0 if block ~ ~ ~ minecraft:light run setblock ~ ~ ~ minecraft:air
execute if score @s dv.ltl matches ..0 run kill @s
''')
    F('luz/apagar', '''
scoreboard players set @s dv.luz 0
scoreboard players operation #pid dv.tmp = @s dv.pid
execute as @e[type=marker,tag=dv_luzmk] if score @s dv.pid = #pid dv.tmp run scoreboard players set @s dv.ltl 0
''')

    # ================================================================== SALIDAS DE LOS SUEÑOS
    c.on('second', 'execute as @e[type=interaction,tag=dv_puerta_sueno] run data merge entity @s {width:1.6f,height:2.8f}')
    c.on('tick', 'execute as @a[predicate=canon:en_sueno] at @s if entity @e[type=interaction,tag=dv_puerta_sueno,distance=..1.4] run function canon:sueno/wake')
    c.patch('sueno/arrived', lambda s: s if 'detrás de ti' in s else s.rstrip('\n') +
            '\ntellraw @s {"text":"(La puerta para despertar está detrás de ti. Crúzala o haz clic en ella.)","color":"gray","italic":true}\n')

    # ================================================================== CÁMARA DE DIANA: mirar su cara real
    c.patch('diana/look_marker', lambda s: '''scoreboard players operation #id dv.tmp = @s dv.id
execute store result score #by dv.tmp run data get entity @s Pos[1] 1000
scoreboard players set #py dv.tmp -1
execute on passengers if entity @s[tag=dv_head] store result score #py dv.tmp run data get entity @s Pos[1] 1000
execute on passengers if entity @s[tag=dv_head] store result score #hy dv.tmp run data get entity @s transformation.translation[1] 1000
scoreboard players operation #ly dv.tmp = #py dv.tmp
scoreboard players operation #ly dv.tmp += #hy dv.tmp
scoreboard players operation #ly dv.tmp -= #by dv.tmp
scoreboard players add #ly dv.tmp 180
execute if score #py dv.tmp matches -1 run scoreboard players set #ly dv.tmp 1450
execute unless score #ly dv.tmp matches 150..2600 run scoreboard players set #ly dv.tmp 1450
execute as @e[type=marker,tag=dv_dlook] if score @s dv.id = #id dv.tmp run function canon:diana/look_marker_move
''')

    # ================================================================== MIEDO + OSCURIDAD
    bars = '\n'.join(f'bossbar add canon:miedo{i} {{"text":"Miedo","color":"gray"}}\nbossbar set canon:miedo{i} max 100\nbossbar set canon:miedo{i} style notched_10'
                     for i in range(1, 9))
    c.on('load', bars)
    c.on('second', '''
execute if score #miedo dv.cfg matches 1 as @a[gamemode=!spectator,gamemode=!creative] at @s run function canon:miedo/second
execute unless score #miedo dv.cfg matches 1 run function canon:miedo/ocultar
''')
    F('miedo/ocultar', '\n'.join(f'bossbar set canon:miedo{i} visible false' for i in range(1, 9)))
    F('miedo/second', '''
scoreboard players set #dm dv.tmp -2
execute if predicate canon:oscuro run scoreboard players add #dm dv.tmp 3
execute if predicate canon:muy_oscuro unless predicate canon:con_luz unless score @s dv.lint matches 1 run scoreboard players add #dm dv.tmp 3
execute if predicate canon:de_noche run scoreboard players add #dm dv.tmp 1
execute if entity @e[tag=dv_horror,distance=..24] run scoreboard players add #dm dv.tmp 5
execute if entity @e[type=zombie,tag=dv_diana,distance=..32] run scoreboard players add #dm dv.tmp 6
execute if entity @e[type=zombie,tag=dv_devota,distance=..24] run scoreboard players add #dm dv.tmp 3
execute if entity @e[type=#canon:hostiles,distance=..12] run scoreboard players add #dm dv.tmp 1
execute if entity @s[y=-64,dy=104] run scoreboard players add #dm dv.tmp 1
execute if entity @a[distance=0.5..8,gamemode=!spectator] run scoreboard players remove #dm dv.tmp 2
execute if entity @e[type=wolf,tag=dv_luna,distance=..10] run scoreboard players remove #dm dv.tmp 2
execute if predicate canon:iluminado run scoreboard players remove #dm dv.tmp 1
execute if predicate canon:de_dia unless predicate canon:oscuro run scoreboard players remove #dm dv.tmp 2
scoreboard players operation @s dv.miedo += #dm dv.tmp
execute if score @s dv.miedo matches ..-1 run scoreboard players set @s dv.miedo 0
execute if score @s dv.miedo matches 101.. run scoreboard players set @s dv.miedo 100
function canon:miedo/oscuridad
function canon:miedo/barra
execute if score @s dv.miedo matches 50.. run function canon:miedo/alucinar
execute if score @s dv.miedo matches 80.. if score #m40 dv.clock matches 0 run playsound canon:fx.heartbeat_fast ambient @s ~ ~ ~ 0.6 1
execute if score @s dv.miedo matches 60..79 if score #m40 dv.clock matches 0 run playsound canon:fx.heartbeat ambient @s ~ ~ ~ 0.4 1
''')
    lines = []
    for i in range(1, 9):
        F(f'miedo/bar/b{i}', f'''
bossbar set canon:miedo{i} players @s
bossbar set canon:miedo{i} visible true
execute store result bossbar canon:miedo{i} value run scoreboard players get @s dv.miedo
execute if score @s dv.miedo matches ..39 run bossbar set canon:miedo{i} color white
execute if score @s dv.miedo matches 40..69 run bossbar set canon:miedo{i} color yellow
execute if score @s dv.miedo matches 70.. run bossbar set canon:miedo{i} color red
execute if score @s dv.miedo matches ..39 run bossbar set canon:miedo{i} name {{"text":"Miedo","color":"gray"}}
execute if score @s dv.miedo matches 40..69 run bossbar set canon:miedo{i} name {{"text":"Miedo: algo no está bien","color":"yellow"}}
execute if score @s dv.miedo matches 70.. run bossbar set canon:miedo{i} name {{"text":"Miedo: no estás solo","color":"red"}}
''')
        lines.append(f'execute if score @s dv.pid matches {i} run function canon:miedo/bar/b{i}')
    F('miedo/barra', '\n'.join(lines))
    F('miedo/oscuridad', '''
execute if predicate canon:muy_oscuro unless predicate canon:con_luz unless score @s dv.lint matches 1 unless predicate canon:en_sueno unless predicate canon:en_casa_sueno run scoreboard players add @s dv.oscu 1
execute unless predicate canon:muy_oscuro run scoreboard players set @s dv.oscu 0
execute if predicate canon:con_luz run scoreboard players set @s dv.oscu 0
execute if score @s dv.lint matches 1 run scoreboard players set @s dv.oscu 0
execute if score @s dv.oscu matches 6 run title @s actionbar {"text":"Está muy oscuro. Algo se mueve cerca. Necesitas luz.","color":"#c94a4a","italic":true}
execute if score @s dv.oscu matches 6.. run effect give @s minecraft:darkness 3 0 true
execute if score @s dv.oscu matches 10.. if predicate canon:azar/1en4 run playsound canon:devota.whisper ambient @s ^ ^ ^-2 0.6 0.6
execute if score @s dv.oscu matches 18 run tellraw @s {"text":"Algo te muerde en la oscuridad. Prende una antorcha.","color":"#c94a4a","italic":true}
execute if score @s dv.oscu matches 18.. run scoreboard players operation #c dv.tmp = @s dv.oscu
execute if score @s dv.oscu matches 18.. run scoreboard players operation #c dv.tmp %= #3 dv.math
execute if score @s dv.oscu matches 18.. if score #c dv.tmp matches 0 run function canon:miedo/mordida
''')
    F('miedo/mordida', '''
damage @s 2 minecraft:generic
playsound minecraft:entity.phantom.bite hostile @s ^ ^ ^-1 0.8 0.6
particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.1 3 normal
scoreboard players add @s dv.miedo 5
''')
    halluc = [
        'playsound canon:diana.step hostile @s ^ ^ ^-3 0.7 1',
        'playsound minecraft:entity.creeper.primed hostile @s ^1 ^ ^-2 0.8 1',
        'playsound canon:diana.knock hostile @s ^4 ^ ^-4 0.8 1',
        'playsound canon:devota.whisper hostile @s ^-2 ^ ^-1 0.8 0.8',
        'playsound canon:diana.name hostile @s ^ ^ ^-6 0.6 0.9',
        'playsound minecraft:entity.zombie.ambient hostile @s ^-5 ^ ^-3 0.7 0.7',
        'playsound minecraft:block.wooden_door.open block @s ^6 ^ ^-2 0.7 0.9',
        'playsound canon:devota.scream hostile @s ^20 ^ ^20 0.4 0.8',
        'playsound minecraft:entity.spider.ambient hostile @s ^ ^2 ^-1 0.6 0.8',
        'title @s times 0 4 4\ntitle @s subtitle ""\ntitle @s title ["",{"text":"\\ue102","font":"canon:susto","color":"white"}]',
        'execute anchored eyes positioned ^ ^ ^9 run particle minecraft:squid_ink ~ ~-0.6 ~ 0.15 0.7 0.15 0 40 force @s',
        'tellraw @s {"text":"...¿oíste eso?","color":"dark_gray","italic":true}',
    ]
    c.pick('miedo/aluc', halluc)
    F('miedo/alucinar', '''
execute if score @s dv.miedo matches 50..74 if predicate canon:azar/1en40 run function canon:miedo/aluc
execute if score @s dv.miedo matches 75.. if predicate canon:azar/1en20 run function canon:miedo/aluc
execute if score @s dv.miedo matches 90.. if predicate canon:azar/1en60 run function canon:fx/shake_small
''')

    # ================================================================== ACOSO EN TU CASA
    c.on('second', '''
execute if score #acoso dv.cfg matches 1 as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s run function canon:acoso/second
''')
    F('acoso/second', '''
scoreboard players set @s dv.home 0
execute if data entity @s SpawnX if data entity @s {SpawnDimension:"minecraft:overworld"} run function canon:acoso/en_casa
scoreboard players remove @s[scores={dv.hcd=1..}] dv.hcd 1
scoreboard players remove @s[scores={dv.acd=1..}] dv.acd 1
execute if score @s dv.home matches 1 if predicate canon:de_noche unless score @s dv.hcd matches 1.. unless data entity @s SleepingX if predicate canon:azar/1en100 run function canon:acoso/evento
execute if score @s dv.home matches 1 if predicate canon:de_noche unless score @s dv.hcd matches 1.. unless data entity @s SleepingX if score @s dv.miedo matches 50.. if predicate canon:azar/1en60 run function canon:acoso/evento
function canon:acecho/second
''')
    F('acoso/en_casa', '''
execute store result score #hx dv.tmp run data get entity @s SpawnX
execute store result score #hy dv.tmp run data get entity @s SpawnY
execute store result score #hz dv.tmp run data get entity @s SpawnZ
execute store result score #px dv.tmp run data get entity @s Pos[0]
execute store result score #py dv.tmp run data get entity @s Pos[1]
execute store result score #pz dv.tmp run data get entity @s Pos[2]
scoreboard players operation #px dv.tmp -= #hx dv.tmp
scoreboard players operation #py dv.tmp -= #hy dv.tmp
scoreboard players operation #pz dv.tmp -= #hz dv.tmp
execute if score #px dv.tmp matches -12..12 if score #pz dv.tmp matches -12..12 if score #py dv.tmp matches -6..8 run scoreboard players set @s dv.home 1
''')
    F('acoso/evento', '''
scoreboard players set @s dv.hcd 140
scoreboard players add @s dv.miedo 10
function canon:acoso/elegir
''')
    c.pick('acoso/elegir', [
        'function canon:acoso/ventana', 'function canon:acoso/ventana', 'function canon:acoso/puerta',
        'function canon:acoso/techo', 'function canon:acoso/detras', 'function canon:acoso/luces'])
    # ventana: rayos horizontales desde los ojos hasta encontrar vidrio
    F('acoso/ventana', '''
scoreboard players set #vf dv.tmp 0
scoreboard players operation #pid dv.tmp = @s dv.pid
''' + '\n'.join(f'execute if score #vf dv.tmp matches 0 anchored eyes rotated ~{a} 0 positioned ^ ^ ^1 run function canon:acoso/vray_ini' for a in (0, 45, -45, 90, -90, 135, -135, 180)) + '''
execute if score #vf dv.tmp matches 0 run function canon:acoso/puerta
''')
    F('acoso/vray_ini', 'scoreboard players set #vs dv.tmp 0\nfunction canon:acoso/vray')
    F('acoso/vray', '''
scoreboard players add #vs dv.tmp 1
execute if block ~ ~ ~ #canon:vidrio positioned ^ ^ ^1 if block ~ ~ ~ #canon:pasable positioned ~ ~-1.5 ~ run function canon:acoso/asomar
execute if score #vf dv.tmp matches 0 if score #vs dv.tmp matches ..12 if block ~ ~ ~ #canon:pasable positioned ^ ^ ^1 run function canon:acoso/vray
''')
    F('acoso/asomar', '''
scoreboard players set #vf dv.tmp 1
function canon:acecho/elegir_quien
function canon:acecho/aparecer
playsound minecraft:block.glass.hit hostile @a[distance=..16] ~ ~1.5 ~ 0.8 0.6
''')
    F('acoso/puerta', '''
scoreboard players set #vf dv.tmp 0
''' + '\n'.join(f'execute if score #vf dv.tmp matches 0 anchored eyes rotated ~{a} 0 positioned ^ ^-1 ^1 run function canon:acoso/dray_ini' for a in (0, 90, -90, 180, 45, -45, 135, -135)) + '''
execute if score #vf dv.tmp matches 0 run playsound canon:diana.knock hostile @s ^ ^ ^-6 1 0.8
''')
    F('acoso/dray_ini', 'scoreboard players set #vs dv.tmp 0\nfunction canon:acoso/dray')
    F('acoso/dray', '''
scoreboard players add #vs dv.tmp 1
execute if block ~ ~ ~ #minecraft:doors align xyz positioned ~0.5 ~0.5 ~0.5 run function canon:acoso/golpes
execute if score #vf dv.tmp matches 0 if score #vs dv.tmp matches ..14 unless block ~ ~ ~ #minecraft:doors if block ~ ~ ~ #canon:pasable positioned ^ ^ ^1 run function canon:acoso/dray
''')
    F('acoso/golpes', '''
scoreboard players set #vf dv.tmp 1
summon minecraft:marker ~ ~ ~ {Tags:["dv_golpe"]}
''')
    c.on('tick', 'execute as @e[type=marker,tag=dv_golpe] at @s run function canon:acoso/golpe_tick')
    c.pick('acoso/voz_puerta', [
        'tellraw @a[distance=..16] {"text":"Al otro lado de la puerta: «Abre. Soy yo.»","color":"#c94a4a","italic":true}',
        'tellraw @a[distance=..16] {"text":"Al otro lado de la puerta: «Mijito, ábrale a la abuela.»","color":"#c94a4a","italic":true}',
        'tellraw @a[distance=..16] {"text":"Al otro lado de la puerta, alguien respira contra la madera.","color":"#c94a4a","italic":true}',
        'tellraw @a[distance=..16] {"text":"Al otro lado de la puerta: «¿Has visto a Juan?»","color":"#c94a4a","italic":true}'])
    F('acoso/golpe_tick', '''
scoreboard players add @s dv.timer 1
execute if score @s dv.timer matches 1 run playsound canon:diana.knock hostile @a[distance=..20] ~ ~ ~ 1 1
execute if score @s dv.timer matches 14 run playsound canon:diana.knock hostile @a[distance=..20] ~ ~ ~ 1 0.95
execute if score @s dv.timer matches 28 run playsound canon:diana.knock hostile @a[distance=..20] ~ ~ ~ 1 0.9
execute if score @s dv.timer matches 60 run function canon:acoso/voz_puerta
execute if score @s dv.timer matches 90 run playsound minecraft:entity.zombie.attack_wooden_door hostile @a[distance=..20] ~ ~ ~ 0.8 0.7
execute if score @s dv.timer matches 95.. run kill @s
''')
    F('acoso/techo', '''
summon minecraft:marker ~ ~4 ~ {Tags:["dv_techo"]}
''')
    c.on('tick', 'execute as @e[type=marker,tag=dv_techo] at @s run function canon:acoso/techo_tick')
    F('acoso/techo_tick', '''
scoreboard players add @s dv.timer 1
execute if score @s dv.timer matches 1 run tp @s ~-4 ~ ~-3
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #8 dv.math
execute if score #c dv.tmp matches 0 run tp @s ~0.5 ~ ~0.4
execute if score #c dv.tmp matches 0 run playsound minecraft:block.wood.step hostile @a[distance=..14] ~ ~ ~ 1 0.6
execute if score @s dv.timer matches 90 run playsound canon:diana.crawl hostile @a[distance=..14] ~ ~ ~ 1 0.8
execute if score @s dv.timer matches 100.. run kill @s
''')
    F('acoso/detras', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-4 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:acecho/aparecer_aqui
kill @e[type=marker,tag=dv_spot]
playsound canon:diana.breath hostile @s ^ ^ ^-2 0.9 0.8
''')
    F('acecho/aparecer_aqui', 'function canon:acecho/elegir_quien\nfunction canon:acecho/aparecer')
    F('acoso/luces', '''
effect give @s minecraft:darkness 3 0 true
playsound canon:fx.blackout ambient @s ~ ~ ~ 0.8 1
tellraw @s {"text":"Las luces de la casa parpadean. Por un segundo hay alguien más en el cuarto.","color":"#c94a4a","italic":true}
execute anchored eyes positioned ^2 ^ ^5 run particle minecraft:squid_ink ~ ~-0.8 ~ 0.15 0.7 0.15 0 40 force @s
''')

    # ================================================================== EL QUE SE ASOMA (rig genérico de acecho)
    for key, (body, hd, sc) in PEEK.items():
        F(f'acecho/rig_{key}', rig_summon(['dv_asomo', 'dv_horror', f'dv_as_{key}'], '???', '#555555', head=hd is not None, scale=sc) + '\n'
          f'execute as @e[type=zombie,tag=dv_new,tag=dv_asomo,distance=..2,limit=1,sort=nearest] at @s run function canon:acecho/init_{key}')
        F(f'acecho/init_{key}', f'''
function canon:rig/init_common
{set_cmd('body', body)}
{head(hd) if hd else ''}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.watch 0
''')
    c.pick('acecho/elegir_quien', [f'scoreboard players set #quien dv.tmp {i}' for i in range(1, 7)])
    keys = ['zunga', 'miron', 'nicolas', 'mariana', 'abuela', 'dhumana']
    F('acecho/aparecer', '\n'.join(f'execute if score #quien dv.tmp matches {i + 1} run function canon:acecho/rig_{k}' for i, k in enumerate(keys)))
    c.npc('dv_asomo', 'acecho/tick')
    F('acecho/tick', '''
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..64] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..48,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_wtgt] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
execute if entity @a[tag=dv_wtgt] run function canon:acecho/piensa
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('acecho/piensa', '''
execute if score #m2 dv.clock matches 0 run function canon:x/face
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score @s dv.timer matches 40 if score #seen dv.tmp matches 0 run playsound canon:devota.whisper hostile @a[tag=dv_wtgt] ~ ~ ~ 0.5 0.7
execute if score @s dv.watch matches 4.. run function canon:acecho/visto
execute if entity @a[tag=dv_wtgt,distance=..3] run function canon:acecho/visto
execute if score @s dv.timer matches 240.. run function canon:acecho/se_va
''')
    F('acecho/visto', '''
playsound canon:miron.estatica hostile @a[tag=dv_wtgt] ~ ~ ~ 0.8 0.7
execute if predicate canon:azar/1en4 run playsound canon:diana.scream hostile @a[tag=dv_wtgt] ~ ~ ~ 0.5 1.3
execute as @a[tag=dv_wtgt] run scoreboard players add @s dv.miedo 8
function canon:acecho/se_va
''')
    F('acecho/se_va', 'particle minecraft:large_smoke ~ ~1.2 ~ 0.3 0.8 0.3 0.02 20 normal\nfunction canon:rig/despawn')
    c.frames('dv_as_zunga', 'acecho/frames_zunga')
    F('acecho/frames_zunga', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 5
execute if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 6
''')

    # ================================================================== ACECHO EN EL MUNDO
    F('acecho/second', '''
execute unless score @s dv.acd matches 1.. if predicate canon:de_noche if predicate canon:azar/1en300 run function canon:acecho/esquina
execute unless score @s dv.acd matches 1.. if predicate canon:de_noche if score @s dv.miedo matches 40.. if predicate canon:azar/1en150 run function canon:acecho/esquina
execute unless score @s dv.acd matches 1.. if predicate canon:de_dia if predicate canon:azar/1en900 run function canon:acecho/lejos
execute if predicate canon:de_noche if predicate canon:azar/1en240 run function canon:acecho/susurro
execute if entity @s[y=-64,dy=104] if predicate canon:muy_oscuro unless score @s dv.acd matches 1.. if predicate canon:azar/1en150 run function canon:acecho/cueva
execute if entity @s[y=-64,dy=104] if predicate canon:azar/1en80 run function canon:acecho/cueva_sonido
execute if entity @s[y=-64,dy=104] if score #nicolas dv.cfg matches 1 if score @s dv.ncd matches ..0 if predicate canon:azar/1en200 run function canon:nicolas/try
''')
    F('acecho/esquina', '''
scoreboard players set @s dv.acd 90
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #quien dv.tmp 1
execute if predicate canon:azar/1en4 run function canon:acecho/elegir_quien
scoreboard players set #ok dv.tmp 0
execute if predicate canon:azar/50 positioned ^7 ^ ^9 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^-7 ^ ^9 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^ ^ ^-10 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:acecho/aparecer
kill @e[type=marker,tag=dv_spot]
''')
    F('acecho/lejos', '''
scoreboard players set @s dv.acd 300
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #quien dv.tmp 6
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^34 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:acecho/aparecer
kill @e[type=marker,tag=dv_spot]
''')
    c.pick('acecho/susurro', [
        'playsound canon:diana.name hostile @s ^3 ^ ^-3 0.5 0.85\ntitle @s actionbar {"text":"Alguien susurró tu nombre.","color":"#8a7a86","italic":true}',
        'playsound canon:devota.whisper hostile @s ^-3 ^ ^-2 0.6 0.7',
        'playsound canon:diana.breath hostile @s ^ ^ ^-2 0.5 0.9',
        'playsound canon:diana.laugh hostile @s ^12 ^ ^-12 0.4 0.8',
    ])
    F('acecho/cueva', '''
scoreboard players set @s dv.acd 120
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^12 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:acecho/rig_nicolas
kill @e[type=marker,tag=dv_spot]
scoreboard players set #ok dv.tmp 0
execute if predicate canon:azar/50 positioned ^-8 ^ ^-6 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:acecho/rig_nicolas2
kill @e[type=marker,tag=dv_spot]
playsound canon:nicolas.risa hostile @s ^ ^ ^10 0.8 0.8
tellraw @s {"text":"Al fondo del túnel, alguien gordito y de negro te mira. Y otro igual detrás de ti.","color":"#8a8a96","italic":true}
''')
    c.pick('acecho/cueva_sonido', [
        'playsound minecraft:ambient.cave ambient @s ~ ~ ~ 1 1',
        'playsound canon:mina.derrumbe ambient @s ^6 ^2 ^-6 0.7 1',
        'playsound canon:nicolas.pasos hostile @s ^ ^ ^-10 0.7 0.9',
        'playsound canon:nicolas.risa hostile @s ^-12 ^ ^5 0.5 0.7',
        'tellraw @s {"text":"Una voz en la piedra: «Aquí abajo nadie te escucha.»","color":"#8a8a96","italic":true}',
        'playsound minecraft:entity.warden.nearby_close hostile @s ^ ^ ^-8 0.6 1.2',
    ])

    # ================================================================== ZOMBIES TIPO RESIDENT EVIL
    c.on('second', '''
execute as @a[gamemode=!spectator] at @s run function canon:zomb2/herido
''')
    c.on('tick', 'execute if score #zomb_listos dv.cfg matches 1 if score #m10 dv.clock matches 7 run function canon:zomb2/ciclo')
    F('zomb2/herido', 'execute if score #zomb_listos dv.cfg matches 1 if score @s dv.vida < @s dv.vidap run function canon:zomb/senuelo\nscoreboard players operation @s dv.vidap = @s dv.vida')
    F('zomb2/ciclo', '''
execute as @a[gamemode=!spectator] at @s as @e[type=zombie,tag=!dv_brain,distance=..24] at @s run function canon:zomb2/z
execute as @a[gamemode=!spectator] at @s as @e[type=spider,distance=..24] at @s run function canon:zomb2/arana
execute as @e[type=zombie,tag=dv_zmirando] at @s run function canon:zomb2/mirando
''')
    F('zomb2/z', '''
execute if block ~1 ~ ~ #minecraft:wooden_doors run function canon:zomb2/tocar
execute if block ~-1 ~ ~ #minecraft:wooden_doors run function canon:zomb2/tocar
execute if block ~ ~ ~1 #minecraft:wooden_doors run function canon:zomb2/tocar
execute if block ~ ~ ~-1 #minecraft:wooden_doors run function canon:zomb2/tocar
execute if predicate canon:de_noche unless entity @s[tag=dv_zmirando] unless entity @a[distance=..9] if entity @a[gamemode=!spectator,distance=..22] if predicate canon:azar/1en12 run function canon:zomb2/mirar
''')
    F('zomb2/tocar', '''
scoreboard players add @s dv.zkn 1
playsound minecraft:entity.zombie.attack_wooden_door hostile @a[distance=..24] ~ ~ ~ 1 0.9
particle minecraft:block minecraft:oak_planks ~ ~1 ~ 0.4 0.4 0.4 0 6 normal
execute if score #zomb_rompen dv.cfg matches 1 if score @s dv.zkn matches 14.. run function canon:zomb2/romper_puerta
''')
    F('zomb2/romper_puerta', '''
scoreboard players set @s dv.zkn 0
execute if block ~1 ~ ~ #minecraft:wooden_doors run setblock ~1 ~ ~ minecraft:air destroy
execute if block ~-1 ~ ~ #minecraft:wooden_doors run setblock ~-1 ~ ~ minecraft:air destroy
execute if block ~ ~ ~1 #minecraft:wooden_doors run setblock ~ ~ ~1 minecraft:air destroy
execute if block ~ ~ ~-1 #minecraft:wooden_doors run setblock ~ ~ ~-1 minecraft:air destroy
playsound minecraft:entity.zombie.break_wooden_door hostile @a[distance=..32] ~ ~ ~ 1 0.8
''')
    F('zomb2/mirar', '''
tag @s add dv_zmirando
scoreboard players set @s dv.zmira 120
data merge entity @s {NoAI:1b}
execute facing entity @a[gamemode=!spectator,distance=..22,limit=1,sort=nearest] eyes run tp @s ~ ~ ~ ~ ~
''')
    F('zomb2/mirando', '''
scoreboard players remove @s dv.zmira 10
execute facing entity @a[gamemode=!spectator,distance=..30,limit=1,sort=nearest] eyes run tp @s ~ ~ ~ ~ ~
execute if entity @a[gamemode=!spectator,distance=..8] run scoreboard players set @s dv.zmira 0
execute if score @s dv.zmira matches ..0 run function canon:zomb2/soltar
''')
    F('zomb2/soltar', '''
tag @s remove dv_zmirando
data merge entity @s {NoAI:0b}
playsound minecraft:entity.zombie.ambient hostile @a[distance=..24] ~ ~ ~ 1.2 0.6
effect give @s minecraft:speed 5 1 true
''')
    F('zomb2/arana', '''
tag @a remove dv_lookers
tag @a[gamemode=!spectator,distance=..24,limit=1,sort=nearest] add dv_lookers
tag @a[tag=dv_lookers] add dv_wtgt
function canon:x/seen
execute if score #seen dv.tmp matches 0 if entity @a[tag=dv_wtgt,distance=4..] facing entity @a[tag=dv_wtgt,limit=1] feet positioned ^ ^ ^0.6 if block ~ ~ ~ #canon:pasable run tp @s ~ ~ ~ ~ ~
execute if score #seen dv.tmp matches 1 if predicate canon:azar/1en6 run playsound minecraft:entity.spider.ambient hostile @a[tag=dv_wtgt] ~ ~ ~ 0.6 0.6
tag @a remove dv_lookers
tag @a remove dv_wtgt
''')

    # ================================================================== ADMIN
    F('admin/terror/miedo', 'scoreboard players set @s dv.miedo 90\ntellraw @s {"text":"[Canon Event] Miedo al 90.","color":"dark_gray"}')
    F('admin/terror/ventana', 'function canon:acoso/ventana')
    F('admin/terror/puerta', 'function canon:acoso/puerta')
    F('admin/terror/techo', 'function canon:acoso/techo')
    F('admin/terror/esquina', 'scoreboard players set @s dv.acd 0\nfunction canon:acecho/esquina')
    F('admin/terror/cueva', 'scoreboard players set @s dv.acd 0\nfunction canon:acecho/cueva')
    for cmd, d in [('miedo', 'Subir tu miedo a 90 (alucinaciones)'), ('ventana', 'Algo se asoma por tu ventana'), ('puerta', 'Tocan tu puerta'),
                   ('techo', 'Pasos en el techo'), ('esquina', 'Algo te mira desde una esquina'), ('cueva', 'Nicolás en la cueva')]:
        c.admin(f'/function canon:admin/terror/{cmd}', d)
