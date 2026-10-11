"""Herramientas 3x3 (martillo, excavadora), hacha taladora y cámara instantánea.

Martillo / excavadora: mientras el jugador sostiene la herramienta, cada tick un rayo desde los
ojos guarda (en un marker propio, dv_hmk + dv.pid) el bloque que mira. Cuando la estadística
minecraft.used de esa herramienta sube y ese bloque ya es aire, rompe los otros 8 del plano 3x3
(según hacia dónde mira). Agachado = 1 bloque. El hacha taladora rompe todos los troncos unidos.
Recetas: técnica knowledge_book + logro recipe_crafted (las recetas de 1.20.1 no dan NBT).
"""
import json, os
from PIL import Image
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon.ctx import item_nbt, loot_item

TIERS = [('madera', 'wooden', 59, '#a8834a', '#6b4f2a'), ('piedra', 'stone', 131, '#8a8a8a', '#5a5a5a'), ('oro', 'golden', 32, '#f2d24a', '#b8932a'),
         ('hierro', 'iron', 250, '#d8d8d8', '#9a9a9a'), ('diamante', 'diamond', 1561, '#5fe0d2', '#2a9c92'),
         ('netherita', 'netherite', 2031, '#4a3f45', '#2a2328')]
TOOLS = [  # id, base vanilla, nombre, cmd base, objetivo prefijo
    ('martillo', 'pickaxe', 'Martillo', 7312020, 'p'),
    ('excavadora', 'shovel', 'Excavadora', 7312030, 's'),
    ('taladora', 'axe', 'Hacha taladora', 7312040, 'a'),
]
CAM_CMD, FILM_CMD, FOTO_CMD = 7312010, 7312011, 7312012

FOTOS = [  # (clave, tag que la activa, texto de la foto)
    ('doble', 'dv_doppel', 'Esa persona sale borrosa y torcida. No tiene ojos.'),
    ('zunga', 'dv_zunga', 'Una mujer doblada en un ángulo imposible mira a la cámara.'),
    ('diana', 'dv_diana', 'Una mujer doblada en un ángulo imposible mira a la cámara.'),
    ('miron', 'dv_miron', 'Al fondo, una figura negra y flaca. Sus ojos brillan con el flash.'),
    ('devota', 'dv_devota', 'Ella sonríe a la cámara. Te está mirando a ti, no al lente.'),
    ('mariana', 'dv_mariana', 'Mariana, inmóvil. En la foto sí está sonriendo.'),
    ('nicolas', 'dv_nicolas', 'Un chico de negro tapándose la cara. Detrás, piedra y oscuridad.'),
    ('dani', 'dv_dani', 'Dani mira hacia un lado, como si alguien la llamara.'),
    ('dhumana', 'dv_dhum', 'Una chica pálida con ojeras. Detrás de ella hay otra sombra igual.'),
    ('kevin', 'dv_kevin', 'Kevin haciendo una cara ridícula. Sus ojos salieron rojos.'),
    ('juli', 'dv_juli', 'Juli riéndose. La foto huele a flores.'),
    ('luna', 'dv_luna', 'Luna moviendo la cola. Salió movida, pero es perfecta.'),
    ('alto', 'dv_alto', 'Entre los árboles, un hombre altísimo de traje. No tiene cara.'),
    ('amigo', 'player', 'Tu amigo, tranquilo. Detrás de él hay una mano en su hombro.'),
]


def icon(path, kind, head, dark):
    """Ícono 16x16 pixel art de la herramienta."""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    p = im.load()
    H = tuple(int(head[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    D = tuple(int(dark[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    W, Wd = (137, 103, 39, 255), (88, 62, 22, 255)
    for i in range(9):  # mango diagonal
        x, y = 2 + i, 13 - i
        p[x, y] = W
        if y + 1 < 16:
            p[x, y + 1] = Wd
    if kind == 'pickaxe':  # cabeza ancha de martillo 3x3
        for x in range(5, 15):
            for y in range(1, 6):
                if (x - 5) + (5 - y) < 13:
                    p[x, y] = H if (x + y) % 5 else D
        for x in range(6, 14):
            p[x, 5] = D
    elif kind == 'shovel':
        for x in range(8, 15):
            for y in range(1, 8):
                if abs((x - 11) - (y - 4)) < 4:
                    p[x, y] = H if (x * 3 + y) % 7 else D
    else:  # hacha
        for x in range(7, 15):
            for y in range(1, 9):
                if (x - 7) + abs(y - 4) < 9 and x > 8 - (y // 3):
                    p[x, y] = H if (x + 2 * y) % 6 else D
        for y in range(2, 8):
            p[14, y] = D
    im.save(path)


def camera_icon(path):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    p = im.load()
    for x in range(1, 15):
        for y in range(4, 13):
            p[x, y] = (40, 40, 46, 255) if y > 5 else (70, 70, 78, 255)
    for x in range(3, 7):
        p[x, 3] = (70, 70, 78, 255)
    for x in range(5, 11):
        for y in range(6, 12):
            if (x - 7.5) ** 2 + (y - 8.5) ** 2 < 8:
                p[x, y] = (120, 160, 200, 255) if (x - 7) ** 2 + (y - 8) ** 2 < 2 else (20, 20, 24, 255)
    p[12, 6] = (250, 240, 200, 255)
    p[13, 6] = (250, 240, 200, 255)
    im.save(path)


def paper_icon(path, base, accent):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    p = im.load()
    for x in range(2, 14):
        for y in range(2, 14):
            p[x, y] = base
    for x in range(4, 12):
        for y in range(4, 10):
            p[x, y] = accent
    im.save(path)


def item_model(c, name, parent='minecraft:item/handheld'):
    c.json(f'assets/canon/models/item/{name}.json', {'parent': parent, 'textures': {'layer0': f'canon:item/{name}'}})


def build(c):
    shim.use(c)
    c.config('herr3x3', 'Herramientas 3x3 y hacha taladora', 1)
    for t in ('p', 's', 'a'):
        for tier, vid, *_ in TIERS:
            c.objective(f'dv.h{t}{vid[0]}', f'minecraft.used:minecraft.{vid}_{ {"p": "pickaxe", "s": "shovel", "a": "axe"}[t]}')
    c.objective('dv.hok')
    c.objective('dv.hlog')
    c.objective('dv.hrec')
    # tags de bloques
    c.json('data/canon/tags/blocks/herr_aire.json', {'values': ['minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:water',
                                                               'minecraft:lava', 'minecraft:light', 'minecraft:bubble_column']})
    c.json('data/canon/tags/blocks/herr_no.json', {'values': [
        'minecraft:bedrock', 'minecraft:barrier', 'minecraft:end_portal_frame', 'minecraft:reinforced_deepslate', 'minecraft:obsidian',
        'minecraft:crying_obsidian', 'minecraft:respawn_anchor', 'minecraft:spawner', 'minecraft:command_block',
        'minecraft:chain_command_block', 'minecraft:repeating_command_block', 'minecraft:structure_block', 'minecraft:jigsaw',
        'minecraft:chest', 'minecraft:trapped_chest', 'minecraft:barrel', 'minecraft:furnace', 'minecraft:blast_furnace',
        'minecraft:smoker', 'minecraft:ender_chest', '#minecraft:shulker_boxes', 'minecraft:beacon', 'minecraft:enchanting_table',
        'minecraft:anvil', 'minecraft:chipped_anvil', 'minecraft:damaged_anvil', 'minecraft:hopper', 'minecraft:dropper',
        'minecraft:dispenser', 'minecraft:brewing_stand', 'minecraft:lodestone', 'minecraft:netherite_block', 'minecraft:conduit']})
    # -------------------------------------------------------- ítems, modelos, texturas
    for tid, kind, nombre, cmd0, pre in TOOLS:
        for i, (tier, vid, maxd, col, dark) in enumerate(TIERS):
            name = f'{tid}_{tier}'
            icon(c.path(f'assets/canon/textures/item/{name}.png'), kind, col, dark)
            item_model(c, name)
            c.item_model(f'{vid}_{kind}', cmd0 + i, f'canon:item/{name}')
            lore = {'martillo': ['Rompe 3x3 bloques de piedra a la vez.', 'Agáchate para romper solo uno.'],
                    'excavadora': ['Cava 3x3 bloques de tierra y arena.', 'Agáchate para cavar solo uno.'],
                    'taladora': ['Corta un tronco y cae el árbol entero.', 'Agáchate para cortar normal.']}[tid]
            nbt = item_nbt(tid, f'{nombre} de {tier}', {'madera': '#c9a46a', 'piedra': '#b0b0b0', 'oro': '#f2d24a', 'hierro': '#e0e0e0', 'diamante': '#5fe0d2', 'netherita': '#b39bb0'}[tier],
                           lore + ['Hecho en el taller de Valle Quieto.'], cmd0 + i)
            c.json(f'data/canon/loot_tables/herr/{name}.json', loot_item(f'{vid}_{kind}', nbt))
    camera_icon(c.path('assets/canon/textures/item/camara.png'))
    item_model(c, 'camara', 'minecraft:item/handheld_rod')
    c.item_model('carrot_on_a_stick', CAM_CMD, 'canon:item/camara')
    paper_icon(c.path('assets/canon/textures/item/pelicula.png'), (40, 34, 30, 255), (190, 120, 40, 255))
    item_model(c, 'pelicula', 'minecraft:item/generated')
    c.item_model('paper', FILM_CMD, 'canon:item/pelicula')
    paper_icon(c.path('assets/canon/textures/item/foto.png'), (236, 232, 222, 255), (70, 64, 80, 255))
    item_model(c, 'foto', 'minecraft:item/generated')
    c.item_model('paper', FOTO_CMD, 'canon:item/foto')
    c.json('data/canon/loot_tables/camara/camara.json', loot_item('carrot_on_a_stick', item_nbt(
        'camara', 'Cámara instantánea', '#f0d8a8', ['Clic derecho: sacar una foto (gasta película).',
                                                   'El flash espanta lo que no debería estar.', 'La cámara ve lo que el ojo no.'],
        CAM_CMD, 'Unbreakable:1b')))
    c.json('data/canon/loot_tables/camara/pelicula.json', loot_item('paper', item_nbt(
        'pelicula', 'Rollo de película', '#d9a441', ['Para la cámara instantánea.'], FILM_CMD), 4))
    fotos_all = FOTOS + [('fantasma', None, 'En la esquina de la foto hay una chica pálida. No había nadie.'),
                         ('nada', None, 'Un paisaje tranquilo. Demasiado tranquilo.')]
    for key, tag, texto in fotos_all:
        c.json(f'data/canon/loot_tables/camara/foto_{key}.json', loot_item('paper', item_nbt(
            'foto', 'Foto instantánea', '#ece8de', [texto, 'Valle Quieto, 13:11'], FOTO_CMD)))

    # -------------------------------------------------------- recetas (knowledge_book)
    def recipe(rid, pattern, key):
        c.json(f'data/canon/recipes/{rid}.json', {'type': 'minecraft:crafting_shaped', 'category': 'equipment', 'pattern': pattern,
                                                  'key': {k: ({'tag': v[1:]} if v.startswith('#') else {'item': 'minecraft:' + v}) for k, v in key.items()},
                                                  'result': {'item': 'minecraft:knowledge_book', 'count': 1}})
        c.json(f'data/canon/advancements/herr/receta_{rid}.json', {
            'criteria': {'c': {'trigger': 'minecraft:recipe_crafted', 'conditions': {'recipe_id': f'canon:{rid}'}}},
            'rewards': {'function': f'canon:herr/craft/{rid}'}})
        return rid
    mats = {'madera': '#minecraft:logs', 'piedra': 'stone', 'oro': 'gold_block', 'hierro': 'iron_block', 'diamante': 'diamond_block'}
    recipes = []
    for tier, block in mats.items():
        recipes.append((recipe(f'martillo_{tier}', ['BBB', ' S ', ' S '], {'B': block, 'S': 'stick'}), f'herr/martillo_{tier}'))
        recipes.append((recipe(f'excavadora_{tier}', ['B', 'S', 'S'], {'B': block, 'S': 'stick'}), f'herr/excavadora_{tier}'))
        recipes.append((recipe(f'taladora_{tier}', ['BB', 'BS', ' S'], {'B': block, 'S': 'stick'}), f'herr/taladora_{tier}'))
    recipes.append((recipe('martillo_netherita', ['DND', ' S ', ' S '], {'D': 'diamond_block', 'N': 'netherite_ingot', 'S': 'stick'}), 'herr/martillo_netherita'))
    recipes.append((recipe('excavadora_netherita', ['N', 'D', 'S'], {'D': 'diamond_block', 'N': 'netherite_ingot', 'S': 'stick'}), 'herr/excavadora_netherita'))
    recipes.append((recipe('taladora_netherita', ['DN', 'DS', ' S'], {'D': 'diamond_block', 'N': 'netherite_ingot', 'S': 'stick'}), 'herr/taladora_netherita'))
    recipes.append((recipe('camara', ['III', 'GRG', 'III'], {'I': 'iron_ingot', 'G': 'glass_pane', 'R': 'redstone'}), 'camara/camara'))
    c.json('data/canon/recipes/pelicula.json', {'type': 'minecraft:crafting_shapeless', 'category': 'misc',
                                                'ingredients': [{'item': 'minecraft:paper'}, {'item': 'minecraft:paper'},
                                                                {'item': 'minecraft:gunpowder'}, {'item': 'minecraft:ink_sac'}],
                                                'result': {'item': 'minecraft:knowledge_book', 'count': 1}})
    c.json('data/canon/advancements/herr/receta_pelicula.json', {
        'criteria': {'c': {'trigger': 'minecraft:recipe_crafted', 'conditions': {'recipe_id': 'canon:pelicula'}}},
        'rewards': {'function': 'canon:herr/craft/pelicula'}})
    recipes.append(('pelicula', 'camara/pelicula'))
    for rid, loot in recipes:
        F(f'herr/craft/{rid}', f'''
clear @s minecraft:knowledge_book 1
loot give @s loot canon:{loot}
playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 0.8 1.1
advancement revoke @s only canon:herr/receta_{rid}
''')
    F('herr/recetas', '\n'.join(f'recipe give @s canon:{rid}' for rid, _ in recipes) + '\ntag @s add dv_hrecetas')

    # -------------------------------------------------------- lógica por jugador
    held = []
    for tid, kind, nombre, cmd0, pre in TOOLS:
        items = [f'minecraft:{vid}_{kind}' for _, vid, *_ in TIERS]
        c.json(f'data/canon/predicates/herr/{tid}.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {
            'equipment': {'mainhand': {'items': items, 'nbt': '{canon:{id:"%s"}}' % tid}}}})
        for tier, vid, maxd, *_ in TIERS:
            c.json(f'data/canon/predicates/herr/{tid}_{tier}.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                                     'predicate': {'equipment': {'mainhand': {'items': [f'minecraft:{vid}_{kind}'], 'nbt': '{canon:{id:"%s"}}' % tid}}}})
            # gastar 1 de durabilidad (fracción)
            c.json(f'data/canon/item_modifiers/herr/gastar_{tier}.json', {'function': 'minecraft:set_damage', 'damage': round(-1.0 / maxd, 6), 'add': True})
        held.append(tid)
    used_objs = [f'dv.h{p}{vid[0]}' for p in ('p', 's', 'a') for _, vid, *_ in TIERS]
    c.on('player', '\n'.join([
        'execute unless entity @s[tag=dv_hrecetas] run function canon:herr/recetas',
        'scoreboard players set #hb dv.tmp 0',
    ] + [f'execute if score @s {o} matches 1.. run scoreboard players set #hb dv.tmp 1' for o in used_objs]
        + [f'scoreboard players set @s {o} 0' for o in used_objs] + [
        'execute if score #herr3x3 dv.cfg matches 1 if predicate canon:herr/martillo run function canon:herr/tick_martillo',
        'execute if score #herr3x3 dv.cfg matches 1 if predicate canon:herr/excavadora run function canon:herr/tick_excavadora',
        'execute if score #herr3x3 dv.cfg matches 1 if predicate canon:herr/taladora run function canon:herr/tick_taladora',
    ]))
    for tid in ('martillo', 'excavadora', 'taladora'):
        cond = 'if score @s dv.hlog matches 1 ' if tid == 'taladora' else ''
        F(f'herr/tick_{tid}', f'''
execute if score #hb dv.tmp matches 1 if score @s dv.hok matches 1 {cond}unless predicate canon:agachado run function canon:herr/{tid}/romper
function canon:herr/ray
''')
    F('herr/ray', '''
scoreboard players set @s dv.hok 0
scoreboard players set #hstep dv.tmp 0
execute anchored eyes positioned ^ ^ ^ run function canon:herr/ray_step
''')
    F('herr/ray_step', '''
scoreboard players add #hstep dv.tmp 1
execute unless block ~ ~ ~ #canon:herr_aire run function canon:herr/ray_hit
execute if block ~ ~ ~ #canon:herr_aire if score #hstep dv.tmp matches ..50 positioned ^ ^ ^0.1 run function canon:herr/ray_step
''')
    F('herr/ray_hit', '''
scoreboard players set @s dv.hok 1
scoreboard players set @s dv.hlog 0
execute if block ~ ~ ~ #minecraft:logs run scoreboard players set @s dv.hlog 1
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #hf dv.tmp 0
execute align xyz positioned ~0.5 ~0.5 ~0.5 as @e[type=marker,tag=dv_hmk] if score @s dv.pid = #pid dv.tmp run function canon:herr/mk_move
execute if score #hf dv.tmp matches 0 align xyz positioned ~0.5 ~0.5 ~0.5 run function canon:herr/mk_new
''')
    F('herr/mk_move', 'tp @s ~ ~ ~\nscoreboard players set #hf dv.tmp 1')
    F('herr/mk_new', '''
summon minecraft:marker ~ ~ ~ {Tags:["dv_hmk","dv_hmk_new"]}
scoreboard players operation @e[type=marker,tag=dv_hmk_new] dv.pid = #pid dv.tmp
tag @e[type=marker,tag=dv_hmk_new] remove dv_hmk_new
''')
    # plano según la mirada del jugador dv_hbreaker -> #plane (0: x/y, 1: z/y, 2: x/z)
    F('herr/plano', '''
scoreboard players set #plane dv.tmp 0
execute if entity @a[tag=dv_hbreaker,x_rotation=50..90] run scoreboard players set #plane dv.tmp 2
execute if entity @a[tag=dv_hbreaker,x_rotation=-90..-50] run scoreboard players set #plane dv.tmp 2
execute if score #plane dv.tmp matches 0 if entity @a[tag=dv_hbreaker,y_rotation=-135..-45] run scoreboard players set #plane dv.tmp 1
execute if score #plane dv.tmp matches 0 if entity @a[tag=dv_hbreaker,y_rotation=45..135] run scoreboard players set #plane dv.tmp 1
''')
    offs = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
    for tid, tagb in (('martillo', '#minecraft:mineable/pickaxe'), ('excavadora', '#minecraft:mineable/shovel')):
        F(f'herr/{tid}/romper', f'''
tag @s add dv_hbreaker
scoreboard players set #hn dv.tmp 0
scoreboard players operation #pid dv.tmp = @s dv.pid
execute as @e[type=marker,tag=dv_hmk] if score @s dv.pid = #pid dv.tmp at @s if block ~ ~ ~ #canon:herr_aire run function canon:herr/{tid}/area
function canon:herr/gastar
tag @s remove dv_hbreaker
''')
        lines = ['function canon:herr/plano']
        for a, b in offs:
            lines.append(f'execute if score #plane dv.tmp matches 0 positioned ~{a} ~{b} ~ run function canon:herr/{tid}/uno')
            lines.append(f'execute if score #plane dv.tmp matches 1 positioned ~ ~{b} ~{a} run function canon:herr/{tid}/uno')
            lines.append(f'execute if score #plane dv.tmp matches 2 positioned ~{a} ~ ~{b} run function canon:herr/{tid}/uno')
        F(f'herr/{tid}/area', '\n'.join(lines))
        F(f'herr/{tid}/uno', f'execute if block ~ ~ ~ {tagb} unless block ~ ~ ~ #canon:herr_no run function canon:herr/romper_bloque')
    F('herr/romper_bloque', 'setblock ~ ~ ~ minecraft:air destroy\nscoreboard players add #hn dv.tmp 1')
    # hacha taladora
    F('herr/taladora/romper', '''
tag @s add dv_hbreaker
scoreboard players set #hn dv.tmp 0
scoreboard players operation #pid dv.tmp = @s dv.pid
execute as @e[type=marker,tag=dv_hmk] if score @s dv.pid = #pid dv.tmp at @s if block ~ ~ ~ #canon:herr_aire run function canon:herr/taladora/vecinos
execute if score #hn dv.tmp matches 1.. run playsound minecraft:block.wood.break block @a[distance=..24] ~ ~ ~ 1 0.6
function canon:herr/gastar
tag @s remove dv_hbreaker
''')
    vec = [(dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) if (dx, dy, dz) != (0, 0, 0)]
    F('herr/taladora/vecinos', '\n'.join(
        f'execute if score #hn dv.tmp matches ..199 positioned ~{dx} ~{dy} ~{dz} if block ~ ~ ~ #minecraft:logs run function canon:herr/taladora/paso'
        for dx, dy, dz in vec))
    F('herr/taladora/paso', 'setblock ~ ~ ~ minecraft:air destroy\nscoreboard players add #hn dv.tmp 1\nfunction canon:herr/taladora/vecinos')
    # durabilidad (como el jugador dv_hbreaker): 1 por bloque extra
    F('herr/gastar', '''
execute if entity @s[gamemode=creative] run scoreboard players set #hn dv.tmp 0
execute if score #hn dv.tmp matches 1.. run function canon:herr/gastar_uno
execute store result score #hdmg dv.tmp run data get entity @s SelectedItem.tag.Damage
scoreboard players set #hmax dv.tmp 99999
''' + '\n'.join(f'execute if predicate canon:herr/{t}_{tier} run scoreboard players set #hmax dv.tmp {maxd}' for t in ('martillo', 'excavadora', 'taladora') for tier, vid, maxd, *_ in TIERS) + '''
execute if score #hdmg dv.tmp >= #hmax dv.tmp run function canon:herr/se_rompe
''')
    F('herr/gastar_uno', '\n'.join(
        [f'execute if predicate canon:herr/{t}_{tier} run item modify entity @s weapon.mainhand canon:herr/gastar_{tier}'
         for t in ('martillo', 'excavadora', 'taladora') for tier, *_ in TIERS]
        + ['scoreboard players remove #hn dv.tmp 1', 'execute if score #hn dv.tmp matches 1.. run function canon:herr/gastar_uno']))
    F('herr/se_rompe', '''
item replace entity @s weapon.mainhand with minecraft:air
playsound minecraft:entity.item.break player @a[distance=..16] ~ ~ ~ 1 0.9
particle minecraft:crit ~ ~1.2 ~ 0.3 0.3 0.3 0.1 12 normal
''')

    # -------------------------------------------------------- cámara
    c.use_item('camara', 'camara/usar', cooldown=True)
    F('camara/usar', '''
scoreboard players set @s dv.cool 30
execute store result score #film dv.tmp run clear @s minecraft:paper{canon:{id:"pelicula"}} 0
execute if score #film dv.tmp matches 0 run tellraw @s {"text":"No tienes película. (Rollo de película: 2 papeles + pólvora + tinta)","color":"gray","italic":true}
execute if score #film dv.tmp matches 0 run playsound minecraft:block.lever.click player @s ~ ~ ~ 1 1.6
execute if score #film dv.tmp matches 1.. run function canon:camara/disparar
''')
    radios = [(3, 2.5), (7, 4), (12, 6), (18, 8), (26, 10), (36, 13)]
    excl = 'type=!item_display,type=!block_display,type=!text_display,type=!interaction,type=!marker,type=!item,type=!experience_orb,tag=!dv_cam_yo'
    F('camara/cono', '\n'.join(f'execute anchored eyes positioned ^ ^ ^{d} run tag @e[distance=..{r},{excl}] add dv_cam_in' for d, r in radios))
    sel = lambda t: f'@e[tag=dv_cam_in,type={t}]' if t == 'player' else f'@e[tag=dv_cam_in,tag={t}]'
    foto_lines = ['scoreboard players set #fc dv.tmp 0']
    for i, (key, tag, _) in enumerate(FOTOS):
        foto_lines.append(f'execute if score #fc dv.tmp matches 0 if entity {sel(tag)} run scoreboard players set #fc dv.tmp {i + 1}')
    foto_lines.append(f'execute if score #fc dv.tmp matches 0 if predicate canon:azar/1en12 run scoreboard players set #fc dv.tmp {len(FOTOS) + 1}')
    foto_lines.append(f'execute if score #fc dv.tmp matches 0 run scoreboard players set #fc dv.tmp {len(FOTOS) + 2}')
    for i, (key, *_r) in enumerate(fotos_all):
        foto_lines.append(f'execute if score #fc dv.tmp matches {i + 1} run loot give @s loot canon:camara/foto_{key}')
    F('camara/foto', '\n'.join(foto_lines))
    F('camara/disparar', '''
clear @s minecraft:paper{canon:{id:"pelicula"}} 1
tag @s add dv_cam_yo
playsound minecraft:block.dispenser.dispense player @a[distance=..16] ~ ~ ~ 0.9 2
playsound minecraft:entity.item_frame.add_item player @a[distance=..16] ~ ~ ~ 1 1.4
execute anchored eyes positioned ^ ^ ^1.2 run particle minecraft:flash ~ ~ ~ 0 0 0 0 1 force @a[distance=..48]
execute anchored eyes positioned ^ ^ ^4 run particle minecraft:end_rod ~ ~ ~ 1.2 1 1.2 0.15 25 normal
function canon:camara/cono
effect give @e[tag=dv_cam_in,type=!player] minecraft:glowing 3 0 true
execute if score #apagon dv.tmp matches 1 run effect give @s minecraft:night_vision 6 0 true
execute as @e[tag=dv_cam_in,tag=dv_miron] at @s run function canon:camara/espanta
execute as @e[tag=dv_cam_in,tag=dv_zunga] at @s run function canon:camara/espanta
execute as @e[tag=dv_cam_in,tag=dv_doppel] at @s run function canon:camara/revela
execute as @e[tag=dv_cam_in,tag=dv_alto] at @s run function canon:camara/espanta
execute if entity @e[tag=dv_cam_in,tag=dv_diana] run playsound canon:diana.scream hostile @s ~ ~ ~ 0.6 1.4
execute if entity @e[tag=dv_cam_in,tag=dv_diana] run title @s actionbar {"text":"Con el flash, ella retrocede. Por ahora.","color":"#c94a4a","italic":true}
function canon:camara/foto
tag @e[tag=dv_cam_in] remove dv_cam_in
tag @s remove dv_cam_yo
''')
    F('camara/espanta', '''
particle minecraft:large_smoke ~ ~1.2 ~ 0.3 0.8 0.3 0.02 25 normal
playsound canon:miron.grito hostile @a[distance=..24] ~ ~ ~ 0.8 1.3
function canon:rig/despawn
''')
    F('camara/revela', '''
tag @s add dv_revealed
playsound canon:diana.scream hostile @a[distance=..32] ~ ~ ~ 1 1.2
tellraw @a[distance=..32] {"text":"En el flash, la cara de esa persona se derrite. No era quien parecía.","color":"#c94a4a","italic":true}
particle minecraft:soul ~ ~1.2 ~ 0.3 0.8 0.3 0.03 20 normal
function canon:rig/vanish
''')
    # ajustes / admin
    F('admin/herr/kit', '\n'.join(f'loot give @s loot canon:herr/{t}_{tier}' for t in ('martillo', 'excavadora', 'taladora')
                                  for tier, *_ in TIERS) + '\nloot give @s loot canon:camara/camara\nloot give @s loot canon:camara/pelicula')
    F('admin/herr/camara', 'loot give @s loot canon:camara/camara\nloot give @s loot canon:camara/pelicula\nloot give @s loot canon:camara/pelicula')
    c.admin('/function canon:admin/herr/kit', 'Herramientas 3x3, hachas taladoras y cámara')
    c.admin('/function canon:admin/herr/camara', 'Cámara con 8 rollos de película')
