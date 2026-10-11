"""EL MÁS ALLÁ (inspirado en Insidious): si duermes con mucho miedo, o usas la Vela del Más Allá,
tu espíritu sale del cuerpo a un lugar oscuro de niebla roja. Hay fantasmas (transparentes) que
susurran y un demonio de cara roja que te caza. Hay 4 puertas rojas: solo una te devuelve a tu cuerpo.
"""
import json, os
from PIL import Image
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon import skins as S
from canon.ctx import item_nbt, loot_item

DOORS = [(0, 64), (64, 0), (0, -64), (-64, 0)]
GHOST1 = dict(skin='#c8d4dc', hair='#e8eef2', hair_style='long', eyes='#101820', top='#dde6ec', top_style='long', pants='#dde6ec',
              pants_style='long_dress', shoes='#c8d4dc', lips='#8a9aa8', extras=['dark_circles'], alpha=150)
GHOST2 = dict(skin='#b8c4cc', hair='#9aa8b2', hair_style='short', eyes='#101820', top='#5a6670', top_style='jacket', top2='#c8d4dc',
              pants='#4a5660', shoes='#3a4650', lips='#7a8a98', extras=['tie'], alpha=140)
DEMON = dict(skin='#7a0a0a', hair='#0a0808', hair_style='long', eyes='#000000', brows='#000000', top='#0e0c0e', top_style='long',
             pants='#0e0c0e', shoes='#050505', lips='#000000', extras=['makeup'])
MC = '#c94a4a'


def demon_horns(out):
    tex = os.path.join(out, 'assets', 'canon', 'textures', 'item', 'modelo')
    for f in os.listdir(tex):
        if f.startswith('demonio_skin'):
            im = Image.open(os.path.join(tex, f)).convert('RGBA')
            for x in range(0, 4):
                for y in range(0, 4):
                    im.putpixel((x, y), (30 + 10 * x, 8, 8, 255))
            im.save(os.path.join(tex, f))
    md = os.path.join(out, 'assets', 'canon', 'models', 'modelo')
    for f in os.listdir(md):
        if f.startswith('demonio_cabeza'):
            m = json.load(open(os.path.join(md, f)))
            uv = {k: {'uv': [0, 0, 1, 1], 'texture': '#0'} for k in ('north', 'south', 'east', 'west', 'up', 'down')}
            m['elements'].append({'from': [4.5, 16.5, 7], 'to': [6, 21, 8.5], 'faces': uv, 'name': 'cuerno_l',
                                  'rotation': {'angle': 22.5, 'axis': 'z', 'origin': [5, 17, 8]}})
            m['elements'].append({'from': [10, 16.5, 7], 'to': [11.5, 21, 8.5], 'faces': uv, 'name': 'cuerno_r',
                                  'rotation': {'angle': -22.5, 'axis': 'z', 'origin': [11, 17, 8]}})
            json.dump(m, open(os.path.join(md, f), 'w'), separators=(',', ':'))


def build(c):
    shim.use(c)
    g1b, g1h = S.build_character('fantasma1', GHOST1, c.out, ('idle', 'walk_a', 'walk_b', 'reach'), ('neutral', 'void'))
    g2b, g2h = S.build_character('fantasma2', GHOST2, c.out, ('idle', 'walk_a', 'walk_b', 'reach'), ('neutral', 'void'))
    db, dh = S.build_character('demonio', DEMON, c.out, ('idle', 'walk_a', 'walk_b', 'reach', 'run_a', 'run_b'), ('creepy', 'void'))
    demon_horns(c.out)
    shim.models(g1b + g1h, 7321020)
    shim.models(g2b + g2h, 7321030)
    shim.models(db + dh, 7321040)
    K = shim.CMD
    c.config('masalla', 'El Más Allá (al dormir con miedo)', 1)
    c.objective('dv.matime')
    for n in (4, 12, 20, 40):
        c.const(n)
    # ---------------------------------------------------------- dimensión
    c.json('data/canon/dimension_type/mas_alla.json', {
        'ultrawarm': False, 'natural': False, 'coordinate_scale': 1.0, 'has_skylight': False, 'has_ceiling': False, 'ambient_light': 0.0,
        'fixed_time': 18000, 'monster_spawn_light_level': 0, 'monster_spawn_block_light_limit': 0, 'piglin_safe': False, 'bed_works': False,
        'respawn_anchor_works': False, 'has_raids': False, 'logical_height': 256, 'min_y': 0, 'height': 256,
        'infiniburn': '#minecraft:infiniburn_overworld', 'effects': 'minecraft:overworld'})
    c.json('data/canon/worldgen/biome/mas_alla.json', {
        'has_precipitation': False, 'temperature': 0.5, 'downfall': 0.0,
        'effects': {'fog_color': 2621440, 'sky_color': 0, 'water_color': 3342336, 'water_fog_color': 1310720,
                    'ambient_sound': 'minecraft:ambient.soul_sand_valley.loop',
                    'mood_sound': {'sound': 'minecraft:ambient.soul_sand_valley.mood', 'tick_delay': 3000, 'block_search_extent': 8, 'offset': 2.0},
                    'particle': {'options': {'type': 'minecraft:ash'}, 'probability': 0.03}},
        'spawners': {}, 'spawn_costs': {}, 'carvers': {}, 'features': []})
    c.json('data/canon/dimension/mas_alla.json', {'type': 'canon:mas_alla', 'generator': {'type': 'minecraft:flat', 'settings': {
        'biome': 'canon:mas_alla', 'lakes': False, 'features': False, 'structure_overrides': [],
        'layers': [{'block': 'minecraft:bedrock', 'height': 1}, {'block': 'minecraft:blackstone', 'height': 30},
                   {'block': 'minecraft:soul_soil', 'height': 1}]}}})
    c.json('data/canon/predicates/en_mas_alla.json', {'condition': 'minecraft:location_check', 'predicate': {'dimension': 'canon:mas_alla'}})
    # ---------------------------------------------------------- vela del Más Allá (ítem)
    VELA = 7311520
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y in range(6, 15):
        for x in range(6, 10):
            im.putpixel((x, y), (40, 30, 34, 255) if x in (6, 9) else (70, 56, 60, 255))
    for (x, y, col) in ((7, 4, (255, 60, 40, 255)), (8, 4, (255, 60, 40, 255)), (7, 3, (255, 140, 60, 255)), (8, 5, (200, 30, 20, 255)), (7, 5, (200, 30, 20, 255))):
        im.putpixel((x, y), col)
    im.save(c.path('assets/canon/textures/item/vela_mas_alla.png'))
    c.json('assets/canon/models/item/vela_mas_alla.json', {'parent': 'minecraft:item/handheld_rod', 'textures': {'layer0': 'canon:item/vela_mas_alla'}})
    c.item_model('carrot_on_a_stick', VELA, 'canon:item/vela_mas_alla')
    c.json('data/canon/loot_tables/masalla/vela.json', loot_item('carrot_on_a_stick', item_nbt(
        'vela_mas_alla', 'Vela del Más Allá', '#c94a4a', ['Clic derecho: tu espíritu sale del cuerpo.', 'Busca la puerta roja para volver.',
                                                       'No mires al de la cara roja.'], VELA, 'Unbreakable:1b')))
    c.json('data/canon/recipes/vela_mas_alla.json', {'type': 'minecraft:crafting_shapeless', 'category': 'misc', 'ingredients': [
        {'item': 'minecraft:candle'}, {'item': 'minecraft:soul_sand'}, {'item': 'minecraft:ender_pearl'}],
        'result': {'item': 'minecraft:knowledge_book', 'count': 1}})
    c.json('data/canon/advancements/masalla/receta_vela.json', {'criteria': {'c': {'trigger': 'minecraft:recipe_crafted', 'conditions': {
        'recipe_id': 'canon:vela_mas_alla'}}}, 'rewards': {'function': 'canon:masalla/craft_vela'}})
    F('masalla/craft_vela', 'clear @s minecraft:knowledge_book 1\nloot give @s loot canon:masalla/vela\nadvancement revoke @s only canon:masalla/receta_vela')
    c.use_item('vela_mas_alla', 'masalla/usar_vela', cooldown=True)
    F('masalla/usar_vela', '''
scoreboard players set @s dv.cool 40
execute if predicate canon:en_mas_alla run tellraw @s {"text":"Ya estás fuera de tu cuerpo.","color":"gray","italic":true}
execute unless predicate canon:en_mas_alla unless predicate canon:en_sueno unless predicate canon:en_casa_sueno run function canon:masalla/entrar
''')
    c.on('player', '''
execute if score #masalla dv.cfg matches 1 if score @s dv.dzz matches 60 if score @s dv.miedo matches 60.. unless predicate canon:en_mas_alla if predicate canon:azar/1en2 run function canon:masalla/entrar
execute if predicate canon:en_mas_alla run function canon:masalla/player
execute if entity @s[tag=dv_ma] unless predicate canon:en_mas_alla run tag @s remove dv_ma
''')
    c.on('load', 'execute unless score #ma_built dv.build matches 0.. run scoreboard players set #ma_built dv.build 0')
    c.on('tick', 'execute if score #ma_built dv.build matches 1 run function canon:masalla/build_try')
    # ---------------------------------------------------------- construir puertas y ruinas
    B = []
    import random
    rng = random.Random(1311)
    for i, (x, z) in enumerate(DOORS):
        B += [f'fill {x - 2} 32 {z - 1} {x + 2} 37 {z + 1} minecraft:red_nether_bricks', f'fill {x - 1} 32 {z - 1} {x + 1} 35 {z + 1} minecraft:air',
              f'setblock {x} 36 {z} minecraft:redstone_lamp[lit=true]', f'setblock {x - 2} 38 {z} minecraft:soul_lantern',
              f'setblock {x + 2} 38 {z} minecraft:soul_lantern']
    for k in range(40):
        x, z = rng.randint(-60, 60), rng.randint(-60, 60)
        if abs(x) < 4 and abs(z) < 4:
            continue
        h = rng.randint(2, 7)
        blk = rng.choice(['minecraft:blackstone_wall', 'minecraft:dark_oak_log', 'minecraft:polished_blackstone_bricks', 'minecraft:crimson_stem'])
        B.append(f'fill {x} 32 {z} {x} {31 + h} {z} {blk}')
        if rng.random() < 0.3:
            B.append(f'setblock {x} {32 + h} {z} minecraft:soul_lantern')
    for k in range(25):
        x, z = rng.randint(-60, 60), rng.randint(-60, 60)
        B.append(f'setblock {x} 32 {z} {rng.choice(["minecraft:wither_rose", "minecraft:skeleton_skull", "minecraft:candle[lit=true,candles=3]", "minecraft:cobweb"])}')
    F('masalla/build_place', '\n'.join('execute in canon:mas_alla run ' + b for b in B) + '''
execute in canon:mas_alla run kill @e[type=interaction,tag=dv_ma_puerta]
''' + '\n'.join(f'execute in canon:mas_alla run summon minecraft:interaction {x}.5 32 {z}.5 {{Tags:["dv_ma_puerta","dv_ma_p{i + 1}","dv_click","dv_npc_click"],width:3.0f,height:4.0f,response:1b}}'
                for i, (x, z) in enumerate(DOORS)) + '''
scoreboard players set #ma_built dv.build 2
execute in canon:mas_alla run forceload remove -70 -70 70 70
''')
    F('masalla/build_try', 'execute in canon:mas_alla if loaded -70 32 -70 if loaded 70 32 70 if loaded -70 32 70 if loaded 70 32 -70 run function canon:masalla/build_place')
    # ---------------------------------------------------------- entrar / salir
    F('masalla/entrar', '''
function canon:travel/store_return
tag @s add dv_ma
scoreboard players set @s dv.matime 0
scoreboard players add @s dv.miedo 10
execute if score #ma_built dv.build matches 0 run function canon:masalla/construir
function canon:masalla/elegir_puerta
execute in canon:mas_alla run tp @s 0.5 32 0.5 0 0
effect give @s minecraft:darkness 4 0 true
effect give @s minecraft:slow_falling 3 0 true
title @s times 20 80 30
title @s subtitle {"text":"Tu cuerpo sigue durmiendo. Encuentra la puerta roja correcta.","color":"#c94a4a","italic":true}
title @s title {"text":"EL MÁS ALLÁ","color":"#8b0000","bold":true}
playsound canon:fx.whoosh_white master @s ~ ~ ~ 1 0.5
playsound minecraft:ambient.soul_sand_valley.mood ambient @s ~ ~ ~ 1 0.6
tellraw @s {"text":"Hay cuatro puertas rojas, una en cada dirección. Solo una te devuelve. No mires mucho al de la cara roja.","color":"gray","italic":true}
''')
    F('masalla/construir', 'scoreboard players set #ma_built dv.build 1\nexecute in canon:mas_alla run forceload add -70 -70 70 70')
    c.pick('masalla/elegir_puerta', [f'scoreboard players set #ma_real dv.dev {i}' for i in range(1, 5)])
    F('masalla/player', '''
scoreboard players add @s dv.matime 1
execute positioned ~ ~1.6 ~ run function canon:luz/poner
execute if score #m20 dv.clock matches 0 run particle minecraft:ash ~ ~1 ~ 8 3 8 0 40 normal @s
execute if score #m40 dv.clock matches 0 if predicate canon:azar/1en4 run playsound canon:devota.whisper ambient @s ^ ^ ^-4 0.6 0.5
execute if score #m40 dv.clock matches 0 run function canon:masalla/poblar
execute if score @s dv.matime matches 1200 run function canon:masalla/demonio_llega
execute if score @s dv.matime matches 6000 run tellraw @s {"text":"Tu cuerpo se está enfriando. Apúrate.","color":"#c94a4a","italic":true}
execute if score @s dv.matime matches 8400.. run function canon:masalla/expulsado
execute if entity @s[y=-64,dy=90] run function canon:masalla/expulsado
''')
    for i in range(1, 5):
        c.click(f'dv_ma_p{i}', f'masalla/puerta{i}')
        F(f'masalla/puerta{i}', f'''
execute if score #ma_real dv.dev matches {i} as @a[tag=dv_talker] at @s run function canon:masalla/volver
execute unless score #ma_real dv.dev matches {i} as @a[tag=dv_talker] at @s run function canon:masalla/falsa
''')
    F('masalla/falsa', '''
playsound minecraft:block.iron_door.close hostile @s ~ ~ ~ 1 0.5
tellraw @s {"text":"La puerta no abre. Detrás, alguien se ríe. Esta no era.","color":"#c94a4a","italic":true}
scoreboard players add @s dv.miedo 15
function canon:masalla/demonio_llega
''')
    F('masalla/volver', '''
tag @s remove dv_ma
function canon:luz/apagar
function canon:util/tp_return
title @s times 5 40 20
title @s subtitle {"text":"Volviste a tu cuerpo. Por ahora.","color":"#f2a7c3","italic":true}
title @s title ["",{"text":"\\ue104","font":"canon:susto","color":"white"}]
playsound canon:fx.wake_gasp player @s ~ ~ ~ 1 1
scoreboard players set @s dv.miedo 30
''')
    F('masalla/expulsado', '''
function canon:x/jumpscare
playsound canon:devota.scream master @s ~ ~ ~ 1 0.5
damage @s 6 minecraft:generic
tellraw @s {"text":"El de la cara roja te arrancó de ahí. Despiertas temblando.","color":"#c94a4a","italic":true}
function canon:masalla/volver
scoreboard players set @s dv.miedo 85
''')
    # ---------------------------------------------------------- fantasmas
    F('masalla/poblar', '''
execute store result score #mg dv.tmp if entity @e[type=zombie,tag=dv_fantasma,distance=..48]
execute if score #mg dv.tmp matches ..5 positioned ^ ^ ^16 run function canon:masalla/fantasma_spot
execute if score #mg dv.tmp matches ..3 positioned ^-14 ^ ^-8 run function canon:masalla/fantasma_spot
''')
    F('masalla/fantasma_spot', '''
scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:masalla/fantasma_elegir
kill @e[type=marker,tag=dv_spot]
''')
    c.pick('masalla/fantasma_elegir', ['function canon:masalla/fantasma1', 'function canon:masalla/fantasma2'])
    for k in (1, 2):
        F(f'masalla/fantasma{k}', rig_summon(['dv_fantasma', f'dv_fant{k}'], 'Alma', '#c8d4dc') + '\n'
          f'execute as @e[type=zombie,tag=dv_new,tag=dv_fant{k},distance=..2,limit=1,sort=nearest] at @s run function canon:masalla/fantasma{k}_init')
        F(f'masalla/fantasma{k}_init', f'''
function canon:rig/init_common
{set_cmd('body', K[f'fantasma{k}_idle'])}
{head(K[f'fantasma{k}_cabeza_neutral'])}
scoreboard players set @s dv.say -1
function canon:x/add_bubble
tp @s ~ ~ ~ ~180 0
''')
    c.npc('dv_fantasma', 'masalla/fantasma_tick')
    F('masalla/fantasma_tick', '''
function canon:x/links_follow
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
execute unless entity @a[distance=..64] run function canon:rig/despawn
tag @a remove dv_wtgt
tag @a[gamemode=!spectator,distance=..7,limit=1,sort=nearest] add dv_wtgt
execute if entity @a[tag=dv_wtgt] if score #m4 dv.clock matches 0 run function canon:x/face
execute if entity @a[tag=dv_wtgt] if score @s dv.say matches ..0 if predicate canon:azar/1en40 run function canon:masalla/fantasma_habla
execute if entity @a[tag=dv_wtgt,distance=..1.5] run function canon:masalla/fantasma_toca
execute if score @s dv.timer matches 1200.. run function canon:masalla/fantasma_va
tag @a remove dv_wtgt
''')
    c.pick('masalla/fantasma_habla', [say('Alma', '#c8d4dc', '#e8f0f4', t, 90, '@a[distance=..10]') for t in [
        '¿Tú también estás muerto?', 'No encuentro la puerta. Llevo años buscando.', 'Él viene. Siempre viene cuando miras.',
        'Mi cuerpo sigue en una cama. Ya nadie lo visita.', 'La puerta correcta está fría. Las otras queman.',
        'No le digas tu nombre. Lo usa.', 'Juli no está aquí. Ella sueña en otro lado.']])
    F('masalla/fantasma_toca', '''
effect give @a[tag=dv_wtgt] minecraft:slowness 3 1 true
scoreboard players add @a[tag=dv_wtgt] dv.miedo 6
playsound minecraft:entity.vex.ambient hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.5
function canon:masalla/fantasma_va
''')
    F('masalla/fantasma_va', 'particle minecraft:soul ~ ~1 ~ 0.3 0.8 0.3 0.02 20 normal\nfunction canon:rig/despawn')
    # ---------------------------------------------------------- el demonio
    F('masalla/demonio_llega', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players operation #me dv.tmp = @s dv.pid
scoreboard players set #dex dv.tmp 0
execute as @e[type=zombie,tag=dv_demonio] if score @s dv.target = #me dv.tmp run scoreboard players set #dex dv.tmp 1
execute if score #dex dv.tmp matches 0 positioned ^ ^ ^-14 run function canon:masalla/demonio_summon
tellraw @s {"text":"Algo con la cara roja salió de la niebla. Te está buscando.","color":"#8b0000","italic":true}
playsound minecraft:entity.warden.emerge hostile @s ^ ^ ^-10 1 0.8
''')
    F('masalla/demonio_summon', rig_summon(['dv_demonio', 'dv_horror'], 'El de la cara roja', '#8b0000', scale=1.05) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_demonio,distance=..2,limit=1,sort=nearest] at @s run function canon:masalla/demonio_init')
    F('masalla/demonio_init', f'''
function canon:rig/init_common
{set_cmd('body', K['demonio_idle'])}
{head(K['demonio_cabeza_creepy'])}
scoreboard players operation @s dv.target = #pid dv.tmp
''')
    c.npc('dv_demonio', 'masalla/demonio_tick')
    c.frames('dv_demonio', 'masalla/demonio_frames')
    c.frames('dv_fantasma', 'masalla/fantasma_frames')
    F('masalla/demonio_tick', '''
tag @s remove dv_xwalk
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..96,predicate=canon:en_mas_alla] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
tag @a[tag=dv_wtgt] add dv_lookers
execute if entity @a[tag=dv_wtgt] run function canon:masalla/demonio_caza
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('masalla/demonio_caza', '''
execute if score #m2 dv.clock matches 0 run function canon:x/face
function canon:x/seen
tag @s add dv_xwalk
execute if score #seen dv.tmp matches 1 run function canon:x/creep
execute if score #seen dv.tmp matches 0 facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.2 run tp @s ~ ~ ~ ~ ~
execute if score #seen dv.tmp matches 0 at @s run function canon:diana/ground
execute if score #seen dv.tmp matches 1 if score #m20 dv.clock matches 0 run scoreboard players add @a[tag=dv_wtgt] dv.miedo 4
execute if score #m40 dv.clock matches 0 run playsound minecraft:entity.warden.heartbeat hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.7
execute if entity @a[tag=dv_wtgt,distance=..1.6] as @a[tag=dv_wtgt] at @s run function canon:masalla/expulsado
execute if entity @a[tag=dv_wtgt,distance=..1.6] run function canon:rig/despawn
''')
    F('masalla/demonio_frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 4
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 5
''')
    F('masalla/fantasma_frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
''')
    F('admin/masalla/entrar', 'function canon:masalla/entrar')
    F('admin/masalla/vela', 'loot give @s loot canon:masalla/vela')
    c.admin('/function canon:admin/masalla/entrar', 'Ir al Más Allá')
    c.admin('/function canon:admin/masalla/vela', 'Vela del Más Allá')
