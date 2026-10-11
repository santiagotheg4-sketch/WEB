"""Extras: menú principal de terror (fondo, frases, música), ítems paranormales (Ojo del médium para ver
a través de las paredes, Crucifijo), comidas colombianas, mascotas (cachorros y gatitos de colores) y la
Armadura del Velador. Todo crafteable (técnica knowledge_book)."""
import math, random
from PIL import Image, ImageDraw, ImageFilter
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon.ctx import item_nbt, loot_item


def icon(path, draw):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    draw(d)
    im.save(path)


def recipe(c, rid, pattern=None, key=None, shapeless=None, loot=None):
    if shapeless:
        r = {'type': 'minecraft:crafting_shapeless', 'category': 'misc', 'ingredients': [{'item': 'minecraft:' + i} for i in shapeless]}
    else:
        r = {'type': 'minecraft:crafting_shaped', 'category': 'misc', 'pattern': pattern, 'key': {k: {'item': 'minecraft:' + v} for k, v in key.items()}}
    r['result'] = {'item': 'minecraft:knowledge_book', 'count': 1}
    c.json(f'data/canon/recipes/{rid}.json', r)
    c.json(f'data/canon/advancements/extras/receta_{rid}.json', {'criteria': {'c': {'trigger': 'minecraft:recipe_crafted', 'conditions': {
        'recipe_id': f'canon:{rid}'}}}, 'rewards': {'function': f'canon:extras/craft/{rid}'}})
    F(f'extras/craft/{rid}', f'clear @s minecraft:knowledge_book 1\nloot give @s loot {loot}\nadvancement revoke @s only canon:extras/receta_{rid}')
    return rid


def panorama(c):
    rng = random.Random(1311)
    for i in range(6):
        W = 512
        im = Image.new('RGB', (W, W))
        d = ImageDraw.Draw(im)
        for y in range(W):
            t = y / W
            if i == 4:
                col = (int(14 + 10 * t), 4, 6)
            elif i == 5:
                col = (8, 6, 6)
            else:
                col = (int(10 + 60 * t ** 2), int(4 + 8 * t), int(8 + 6 * t))
            d.line([(0, y), (W, y)], fill=col)
        if i < 4:
            if i == 0:
                d.ellipse([340, 70, 420, 150], fill=(150, 20, 20))
                d.ellipse([352, 82, 408, 138], fill=(185, 40, 30))
            for k in range(26):
                x = rng.randint(-20, W)
                h = rng.randint(160, 330)
                w = rng.randint(10, 24)
                d.rectangle([x, W - h, x + w, W], fill=(6, 4, 5))
                for b in range(6):
                    by = W - h + b * 30
                    d.line([(x + w // 2, by), (x + w // 2 + rng.randint(-60, 60), by - rng.randint(10, 50))], fill=(6, 4, 5), width=3)
            if i == 1:
                d.polygon([(180, 360), (260, 300), (340, 360)], fill=(10, 7, 8))
                d.rectangle([195, 360, 325, 470], fill=(12, 9, 10))
                d.rectangle([230, 385, 250, 405], fill=(220, 170, 90))
                d.rectangle([272, 385, 292, 405], fill=(30, 20, 20))
                d.rectangle([276, 389, 288, 401], fill=(235, 235, 225))
            if i == 2:
                d.rectangle([250, 300, 262, 470], fill=(4, 3, 4))
                d.ellipse([244, 278, 268, 304], fill=(4, 3, 4))
                d.point([(252, 288), (260, 288)], fill=(255, 255, 240))
            if i == 3:
                d.rectangle([120, 330, 132, 470], fill=(4, 3, 4))
                d.ellipse([114, 306, 138, 332], fill=(4, 3, 4))
                d.rectangle([115, 316, 120, 320], fill=(170, 10, 10))
            d.rectangle([0, W - 40, W, W], fill=(5, 4, 4))
        im = im.filter(ImageFilter.GaussianBlur(1.2))
        fog = Image.new('RGB', (W, W), (40, 12, 14))
        mask = Image.linear_gradient('L').resize((W, W)).point(lambda v: int(v * 0.35))
        im = Image.composite(fog, im, mask)
        im.save(c.path(f'assets/minecraft/textures/gui/title/background/panorama_{i}.png'))


SPLASH = ['¡Lo que tiene que pasar, va a pasar!', '¡Población: 1.311!', '¡No le hables a Mariana!', '¿Has visto a Juan?',
          '¡Te encontré, Bana!', '¡Juli estaba preguntando por Santi!', '¡No mires al de la cara roja!', '¡Prende una antorcha!',
          '¡Kevin volvió! ¿O no?', '¡La abuela te hizo sopita!', '¡Luna te está ladrando a ti!', '¡No duermas con miedo!',
          '¡Algo te mira desde la esquina!', '¡Cierra las ventanas!', '¡Son las 13:11!', '¡Nicolás está en la mina!',
          '¡El Mirón ya te vio!', '¡Un solo deseo!', '¡Valle Quieto te espera!', '¡No abras la puerta!']


def build(c):
    shim.use(c)
    # ------------------------------------------------ menú principal
    panorama(c)
    open(c.path('assets/minecraft/texts/splashes.txt'), 'w', encoding='utf-8').write('\n'.join(SPLASH) + '\n')
    c.json('assets/minecraft/sounds.json', {'music.menu': {'replace': True, 'sounds': [
        {'name': 'canon:music/valle_quieto', 'stream': True}, {'name': 'canon:music/el_sueno', 'stream': True}, {'name': 'canon:music/casa_blanca', 'stream': True}]}})
    c.objective('dv.ojo')
    c.const(20)
    # ------------------------------------------------ ítems paranormales
    OJO, CRUZ = 7311020, 7311021
    icon(c.path('assets/canon/textures/item/ojo_medium.png'), lambda d: (d.ellipse([2, 5, 13, 11], fill=(230, 225, 210, 255)),
                                                                         d.ellipse([5, 5, 10, 11], fill=(120, 20, 30, 255)),
                                                                         d.ellipse([6, 6, 9, 10], fill=(10, 8, 8, 255)),
                                                                         d.point([(6, 6)], fill=(255, 255, 255, 255))))
    icon(c.path('assets/canon/textures/item/crucifijo.png'), lambda d: (d.rectangle([7, 1, 8, 14], fill=(200, 170, 90, 255)),
                                                                        d.rectangle([4, 4, 11, 5], fill=(200, 170, 90, 255)),
                                                                        d.point([(7, 1), (4, 4)], fill=(250, 230, 160, 255))))
    for n in ('ojo_medium', 'crucifijo'):
        c.json(f'assets/canon/models/item/{n}.json', {'parent': 'minecraft:item/handheld_rod', 'textures': {'layer0': f'canon:item/{n}'}})
    c.item_model('carrot_on_a_stick', OJO, 'canon:item/ojo_medium')
    c.item_model('carrot_on_a_stick', CRUZ, 'canon:item/crucifijo')
    c.json('data/canon/loot_tables/extras/ojo_medium.json', loot_item('carrot_on_a_stick', item_nbt(
        'ojo_medium', 'Ojo del Médium', '#c9a2d8', ['Clic derecho: ves a través de las paredes por 10 segundos.', 'Todo lo que respira se ilumina.',
                                                   'Lo que no respira también.'], OJO, 'Unbreakable:1b')))
    c.json('data/canon/loot_tables/extras/crucifijo.json', loot_item('carrot_on_a_stick', item_nbt(
        'crucifijo', 'Crucifijo de la abuela', '#e8c070', ['Clic derecho: aleja lo que te acecha cerca.', 'Se calienta cuando algo malo está cerca.'],
        CRUZ, 'Unbreakable:1b')))
    c.use_item('ojo_medium', 'extras/ojo', cooldown=True)
    c.use_item('crucifijo', 'extras/cruz', cooldown=True)
    F('extras/ojo', '''
scoreboard players set @s dv.cool 400
effect give @e[distance=..40,type=!player,type=!item_display,type=!text_display,type=!interaction,type=!marker,type=!item] minecraft:glowing 10 0 true
effect give @a[distance=0.5..64] minecraft:glowing 10 0 true
playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.5
playsound canon:devota.whisper ambient @s ~ ~ ~ 0.5 0.6
title @s times 2 20 6
title @s subtitle ""
title @s title ["",{"text":"\\ue103","font":"canon:susto","color":"white"}]
scoreboard players add @s dv.miedo 10
execute if entity @e[tag=dv_horror,distance=..40] run tellraw @s {"text":"El Ojo te muestra siluetas que no deberían estar ahí.","color":"#c9a2d8","italic":true}
''')
    F('extras/cruz', '''
scoreboard players set @s dv.cool 600
playsound minecraft:block.bell.resonate player @a[distance=..16] ~ ~ ~ 1 1.4
particle minecraft:end_rod ~ ~1.2 ~ 2 1 2 0.05 60 normal
execute as @e[tag=dv_asomo,distance=..12] at @s run function canon:acecho/se_va
execute as @e[tag=dv_zunga,distance=..12] at @s run function canon:diana2/zunga/se_esfuma
execute as @e[tag=dv_doppel,distance=..12] at @s run function canon:camara/revela
execute as @e[tag=dv_demonio,distance=..10] at @s run function canon:camara/espanta
execute as @e[type=zombie,tag=dv_miron,distance=..12] at @s run function canon:miron/gone
scoreboard players remove @s dv.miedo 25
execute if score @s dv.miedo matches ..-1 run scoreboard players set @s dv.miedo 0
''')
    recipe(c, 'ojo_medium', ['GAG', 'AEA', 'GAG'], {'G': 'gold_ingot', 'A': 'amethyst_shard', 'E': 'ender_eye'}, loot='canon:extras/ojo_medium')
    recipe(c, 'crucifijo', [' G ', 'GSG', ' G '], {'G': 'gold_ingot', 'S': 'stick'}, loot='canon:extras/crucifijo')
    # ------------------------------------------------ comidas
    FOODS = [  # id, nombre, base, cmd, colores, efectos, miedo, receta
        ('arepa', 'Arepa con queso', 'bread', 7311030, ((230, 200, 120), (250, 240, 200)), ['saturation 1 1'], -10, ['wheat', 'milk_bucket', 'egg']),
        ('empanada', 'Empanada', 'bread', 7311031, ((214, 150, 60), (180, 110, 40)), ['regeneration 4 0'], -5, ['wheat', 'cooked_beef', 'potato']),
        ('bunuelo', 'Buñuelo', 'bread', 7311032, ((220, 170, 80), (240, 200, 110)), ['absorption 30 0'], -10, ['wheat', 'egg', 'sugar']),
        ('chocolate', 'Chocolate caliente', 'honey_bottle', 7311033, ((110, 60, 30), (90, 50, 25)), ['regeneration 6 0'], -25, ['cocoa_beans', 'milk_bucket', 'sugar', 'glass_bottle']),
        ('cafe', 'Café de Valle Quieto', 'honey_bottle', 7311034, ((50, 30, 20), (70, 45, 30)), ['speed 60 0', 'haste 60 0'], -15, ['cocoa_beans', 'cocoa_beans', 'sugar', 'glass_bottle']),
        ('aguapanela', 'Aguapanela', 'honey_bottle', 7311035, ((190, 120, 40), (220, 160, 60)), ['resistance 20 0'], -20, ['sugar_cane', 'sugar_cane', 'glass_bottle']),
    ]
    for fid, nom, base, cmd, (c1, c2), efs, dm, ing in FOODS:
        if base == 'bread':
            icon(c.path(f'assets/canon/textures/item/{fid}.png'), lambda d, c1=c1, c2=c2: (d.ellipse([2, 4, 13, 12], fill=c1 + (255,)),
                                                                                           d.ellipse([4, 6, 11, 10], fill=c2 + (255,))))
        else:
            icon(c.path(f'assets/canon/textures/item/{fid}.png'), lambda d, c1=c1, c2=c2: (d.rectangle([4, 4, 11, 14], fill=(240, 240, 235, 255)),
                                                                                           d.rectangle([5, 6, 10, 13], fill=c1 + (255,)),
                                                                                           d.rectangle([11, 7, 13, 11], outline=(240, 240, 235, 255)),
                                                                                           d.point([(6, 2), (8, 1), (9, 3)], fill=(220, 220, 220, 200))))
        c.json(f'assets/canon/models/item/{fid}.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'canon:item/{fid}'}})
        c.item_model(base, cmd, f'canon:item/{fid}')
        c.json(f'data/canon/loot_tables/extras/{fid}.json', loot_item(base, item_nbt(fid, nom, '#e8c9a8', ['Comida de la casa. Quita el miedo.'], cmd), 2))
        c.json(f'data/canon/advancements/extras/comer_{fid}.json', {'criteria': {'c': {'trigger': 'minecraft:consume_item', 'conditions': {
            'item': {'items': ['minecraft:' + base], 'nbt': '{canon:{id:"%s"}}' % fid}}}}, 'rewards': {'function': f'canon:extras/comer/{fid}'}})
        F(f'extras/comer/{fid}', '\n'.join(f'effect give @s minecraft:{e.split()[0]} {e.split()[1]} {e.split()[2]} true' for e in efs) + f'''
scoreboard players remove @s dv.miedo {-dm}
execute if score @s dv.miedo matches ..-1 run scoreboard players set @s dv.miedo 0
title @s actionbar {jt(nom + ': te sientes un poco mejor.', '#e8c9a8', True)}
advancement revoke @s only canon:extras/comer_{fid}
''')
        recipe(c, fid, shapeless=ing, loot=f'canon:extras/{fid}')
    # ------------------------------------------------ mascotas
    PERRO, GATO = 7311040, 7311041
    icon(c.path('assets/canon/textures/item/caja_cachorro.png'), lambda d: (d.rectangle([2, 6, 13, 14], fill=(160, 110, 60, 255)),
                                                                            d.rectangle([2, 6, 13, 7], fill=(120, 80, 40, 255)),
                                                                            d.ellipse([5, 2, 10, 7], fill=(140, 100, 70, 255)),
                                                                            d.point([(6, 4), (9, 4)], fill=(20, 20, 20, 255))))
    icon(c.path('assets/canon/textures/item/caja_gatito.png'), lambda d: (d.rectangle([2, 6, 13, 14], fill=(160, 110, 60, 255)),
                                                                          d.rectangle([2, 6, 13, 7], fill=(120, 80, 40, 255)),
                                                                          d.ellipse([5, 2, 10, 7], fill=(60, 60, 60, 255)),
                                                                          d.polygon([(5, 3), (6, 0), (7, 3)], fill=(60, 60, 60, 255)),
                                                                          d.polygon([(8, 3), (9, 0), (10, 3)], fill=(60, 60, 60, 255)),
                                                                          d.point([(6, 4), (9, 4)], fill=(120, 220, 120, 255))))
    for n, cmd in (('caja_cachorro', PERRO), ('caja_gatito', GATO)):
        c.json(f'assets/canon/models/item/{n}.json', {'parent': 'minecraft:item/handheld_rod', 'textures': {'layer0': f'canon:item/{n}'}})
        c.item_model('carrot_on_a_stick', cmd, f'canon:item/{n}')
    c.json('data/canon/loot_tables/extras/caja_cachorro.json', loot_item('carrot_on_a_stick', item_nbt(
        'caja_cachorro', 'Caja con un cachorro', '#d9a441', ['Clic derecho: sale un perrito para ti.', 'Cada uno tiene su collar.'], PERRO)))
    c.json('data/canon/loot_tables/extras/caja_gatito.json', loot_item('carrot_on_a_stick', item_nbt(
        'caja_gatito', 'Caja con un gatito', '#d9a441', ['Clic derecho: sale un gatito para ti.', 'Negro, naranja, siamés... sorpresa.'], GATO)))
    c.use_item('caja_cachorro', 'extras/cachorro', cooldown=True)
    c.use_item('caja_gatito', 'extras/gatito', cooldown=True)
    colores = [1, 4, 5, 6, 9, 11, 14, 15]
    c.pick('extras/collar', [f'data modify entity @e[type=wolf,tag=dv_mascota_new,limit=1] CollarColor set value {k}b' for k in colores[:8]])
    F('extras/cachorro', '''
scoreboard players set @s dv.cool 20
clear @s minecraft:carrot_on_a_stick{canon:{id:"caja_cachorro"}} 1
summon minecraft:wolf ~ ~ ~ {Tags:["dv_mascota_new"],Age:-24000,PersistenceRequired:1b}
data modify entity @e[type=wolf,tag=dv_mascota_new,limit=1] Owner set from entity @s UUID
function canon:extras/collar
tag @e[type=wolf,tag=dv_mascota_new] remove dv_mascota_new
playsound minecraft:entity.wolf.ambient neutral @a[distance=..12] ~ ~ ~ 1 1.5
particle minecraft:heart ~ ~1 ~ 0.4 0.4 0.4 0 6 normal
tellraw @s {"text":"Un cachorro sale de la caja y te mueve la cola. Es tuyo.","color":"#d9a441","italic":true}
''')
    gatos = ['black', 'red', 'siamese', 'british_shorthair', 'calico', 'persian', 'ragdoll', 'white', 'tabby', 'jellie']
    c.pick('extras/gato_tipo', [f'data modify entity @e[type=cat,tag=dv_mascota_new,limit=1] variant set value "minecraft:{g}"' for g in gatos])
    F('extras/gatito', '''
scoreboard players set @s dv.cool 20
clear @s minecraft:carrot_on_a_stick{canon:{id:"caja_gatito"}} 1
summon minecraft:cat ~ ~ ~ {Tags:["dv_mascota_new"],Age:-24000,PersistenceRequired:1b}
data modify entity @e[type=cat,tag=dv_mascota_new,limit=1] Owner set from entity @s UUID
function canon:extras/gato_tipo
tag @e[type=cat,tag=dv_mascota_new] remove dv_mascota_new
playsound minecraft:entity.cat.ambient neutral @a[distance=..12] ~ ~ ~ 1 1.3
particle minecraft:heart ~ ~1 ~ 0.4 0.4 0.4 0 6 normal
tellraw @s {"text":"Un gatito sale de la caja y se te sube a los pies. Es tuyo.","color":"#d9a441","italic":true}
''')
    recipe(c, 'caja_cachorro', shapeless=['bone', 'bone', 'cooked_beef', 'barrel'], loot='canon:extras/caja_cachorro')
    recipe(c, 'caja_gatito', shapeless=['cod', 'cod', 'string', 'barrel'], loot='canon:extras/caja_gatito')
    # ------------------------------------------------ Armadura del Velador (negra, buena contra el miedo)
    parts = [('casco', 'leather_helmet', 'head', 3, ['LLL', 'L L']), ('pechera', 'leather_chestplate', 'chest', 8, ['L L', 'LLL', 'LLL']),
             ('pantalon', 'leather_leggings', 'legs', 6, ['LLL', 'L L', 'L L']), ('botas', 'leather_boots', 'feet', 3, ['L L', 'L L'])]
    for i, (pid, base, slot, armor, pat) in enumerate(parts):
        nbt = item_nbt('velador_' + pid, f'Velador: {pid}', '#9a9ab0', ['Armadura del que vela de noche.', 'Juego completo: menos miedo y ves en la oscuridad.'], None,
                       f'AttributeModifiers:[{{AttributeName:"generic.armor",Name:"v",Amount:{armor},Operation:0,UUID:[I;1311,{i},1311,{i + 1}],Slot:"{slot}"}},'
                       f'{{AttributeName:"generic.armor_toughness",Name:"t",Amount:2,Operation:0,UUID:[I;1311,{i},1312,{i + 1}],Slot:"{slot}"}}]')
        nbt = nbt.replace('display:{Name:', 'display:{color:1315860,Name:')
        c.json(f'data/canon/loot_tables/extras/velador_{pid}.json', loot_item(base, nbt))
        recipe(c, 'velador_' + pid, pat, {'L': 'phantom_membrane'}, loot=f'canon:extras/velador_{pid}')
    c.json('data/canon/predicates/velador_completo.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {
        'head': {'nbt': '{canon:{id:"velador_casco"}}'}, 'chest': {'nbt': '{canon:{id:"velador_pechera"}}'},
        'legs': {'nbt': '{canon:{id:"velador_pantalon"}}'}, 'feet': {'nbt': '{canon:{id:"velador_botas"}}'}}}})
    c.on('second', '''
execute as @a[predicate=canon:velador_completo] run scoreboard players remove @s dv.miedo 1
execute as @a[predicate=canon:velador_completo] if predicate canon:muy_oscuro run effect give @s minecraft:night_vision 12 0 true
''')
    kit = ['ojo_medium', 'crucifijo', 'caja_cachorro', 'caja_gatito'] + [f[0] for f in FOODS] + [f'velador_{p[0]}' for p in parts]
    F('admin/extras/kit', '\n'.join(f'loot give @s loot canon:extras/{k}' for k in kit))
    c.admin('/function canon:admin/extras/kit', 'Ojo del médium, crucifijo, comidas, mascotas y armadura')
