"""Catálogo de todos los ítems del mod (para modo creativo) y Recetario con todos los crafteos.
Va al final para ver las recetas y loot tables de todos los módulos. Además: Juli aparece menos y al azar,
y el Alto (Slenderman) sí ataca.
"""
import json
import os
import re
from canon.shim import *  # noqa: F401,F403
from canon import shim

CAT = {'para': 'Paranormal', 'rel': 'Historia', 'extras': 'Comida, mascotas y más', 'herr': 'Herramientas', 'camara': 'Cámara',
       'items': 'Objetos', 'masalla': 'Más Allá', 'muebles': 'Muebles', 'deseos': 'Deseos', 'dani': 'Dani', 'diana2': 'Diana'}
TAGS = {'minecraft:logs': 'cualquier tronco', 'minecraft:planks': 'cualquier tabla', 'minecraft:wool': 'cualquier lana',
        'minecraft:stone_tool_materials': 'piedra', 'minecraft:coals': 'carbón'}


def nombre_de(tag_snbt, fallback):
    m = re.search(r"Name:'((?:[^'\\]|\\.)*)'", tag_snbt or '')
    if m:
        try:
            j = json.loads(m.group(1).replace("\\'", "'"))
            if isinstance(j, dict):
                return j.get('text', '') + ''.join(e.get('text', '') for e in j.get('extra', []) if isinstance(e, dict)) or fallback
            if isinstance(j, list):
                return ''.join(e.get('text', '') if isinstance(e, dict) else str(e) for e in j) or fallback
        except Exception:
            pass
    return fallback


def build(c):
    shim.use(c)
    out = c.out
    reg = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'canon', 'registry_1_20_1.json')))
    blocks = set(reg.get('blocks', {}) if isinstance(reg.get('blocks'), dict) else [b if isinstance(b, str) else b.get('name') for b in reg.get('blocks', [])])

    def all_json(prefix):  # lo que hay en disco (base) + lo que los módulos dejaron en memoria
        res = {}
        base = os.path.join(out, prefix)
        for root, _, files in os.walk(base):
            for fn in files:
                if fn.endswith('.json'):
                    try:
                        res[os.path.relpath(os.path.join(root, fn), base)[:-5].replace(os.sep, '/')] = json.load(open(os.path.join(root, fn)))
                    except Exception:
                        pass
        for rel, (obj, _) in c.json_files.items():
            if rel.startswith(prefix + '/') and rel.endswith('.json'):
                res[rel[len(prefix) + 1:-5]] = obj
        return res
    LOOT = all_json('data/canon/loot_tables')
    # ---------------------------------------------------------------- catálogo (todas las loot tables de un ítem con nombre)
    items = []  # (cat, nombre, loot id)
    for rel in sorted(LOOT):
        if rel.startswith('cat/'):
            continue
        if True:
            try:
                d = LOOT[rel]
                pools = d.get('pools', [])
                if len(pools) != 1 or len(pools[0].get('entries', [])) != 1:
                    continue
                e = pools[0]['entries'][0]
                if e.get('type') != 'minecraft:item':
                    continue
                tag = next((f.get('tag') for f in e.get('functions', []) if f.get('function') == 'minecraft:set_nbt'), None)
                if not tag or 'Name:' not in tag:
                    continue
            except Exception:
                continue
            items.append((rel.split('/')[0], nombre_de(tag, rel.split('/')[-1]), 'canon:' + rel))
    seen, uniq = set(), []
    for it in items:  # sin repetidos (mismo nombre en la misma categoría)
        if (it[0], it[1]) not in seen:
            seen.add((it[0], it[1]))
            uniq.append(it)
    items = sorted(uniq, key=lambda x: (x[0], x[1]))
    c.objective('dv.items', 'trigger')
    cats = sorted({x[0] for x in items})
    c.on('player', 'scoreboard players enable @s dv.items\nexecute if score @s dv.items matches 1.. run function canon:cat/usar\n'
         'execute unless entity @s[tag=dv_recetario] run function canon:cat/recetario')
    lines = ['scoreboard players operation #it dv.tmp = @s dv.items', 'scoreboard players set @s dv.items 0',
             'execute if score #it dv.tmp matches 1 run function canon:cat/menu',
             'execute if score #it dv.tmp matches 2 run loot give @s loot canon:cat/recetario',
             'execute if score #it dv.tmp matches 1000.. unless entity @s[gamemode=creative] run tellraw @s {"text":"El catálogo solo da ítems en modo creativo. En supervivencia, craftéalos: mira el Recetario.","color":"gray","italic":true}']
    for k, cat in enumerate(cats):
        lines.append(f'execute if score #it dv.tmp matches {10 + k} run function canon:cat/c{k}')
        ci = [(i, x) for i, x in enumerate(items) if x[0] == cat]
        F(f'cat/c{k}', menu('@s', CAT.get(cat, cat.capitalize()).upper(), '#d77a8a',
                            [(nm, f'/trigger dv.items set {1000 + i}') for i, (_, nm, _) in ci]))
    for i, (_, nm, lid) in enumerate(items):
        lines.append(f'execute if score #it dv.tmp matches {1000 + i} if entity @s[gamemode=creative] run loot give @s loot {lid}')
    F('cat/usar', '\n'.join(lines))
    F('cat/menu', menu('@s', 'CATÁLOGO DE CANON EVENT (elige una sección)', '#d77a8a',
                       [(CAT.get(cat, cat.capitalize()), f'/trigger dv.items set {10 + k}') for k, cat in enumerate(cats)] +
                       [('Recetario (todos los crafteos)', '/trigger dv.items set 2')]))
    c.admin('/trigger dv.items set 1', 'Catálogo de todos los ítems del mod (en creativo te los da)')
    c.admin('/trigger dv.items set 2', 'Recetario: el libro con todos los crafteos (cualquiera)')

    # ---------------------------------------------------------------- recetario (libro con todos los crafteos)
    reward = {}  # receta -> función de premio
    for d in all_json('data/canon/advancements').values():
        if True:
            if True:
                try:
                    for cr in d.get('criteria', {}).values():
                        if cr.get('trigger') == 'minecraft:recipe_crafted':
                            reward[cr['conditions']['recipe_id']] = d.get('rewards', {}).get('function')
                except Exception:
                    pass

    def fn_text(fid):
        p = fid.split(':', 1)[1]
        if p in c.files:
            return c.files[p]
        fp = os.path.join(out, 'data/canon/functions', p + '.mcfunction')
        return open(fp).read() if os.path.exists(fp) else ''

    def loot_name(lid):
        if lid.split(':', 1)[1] not in LOOT:
            return None
        try:
            e = LOOT[lid.split(':', 1)[1]]['pools'][0]['entries'][0]
            tag = next((f.get('tag') for f in e.get('functions', []) if f.get('function') == 'minecraft:set_nbt'), None)
            return nombre_de(tag, None)
        except Exception:
            return None

    def comp(ing):
        if isinstance(ing, list):
            ing = ing[0]
        if 'tag' in ing:
            return {'text': TAGS.get(ing['tag'], ing['tag'].split(':')[1].replace('_', ' '))}
        iid = ing['item'].split(':')[1]
        return {'translate': ('block.minecraft.' if iid in blocks and iid not in ('wheat', 'sweet_berries') else 'item.minecraft.') + iid}

    pages = []
    RECS = all_json('data/canon/recipes')
    for rname in sorted(RECS):
        fn = rname + '.json'
        rid = 'canon:' + rname
        d = RECS[rname]
        res = d.get('result', {})
        res_id = res.get('item', '') if isinstance(res, dict) else ''
        name = None
        if res_id.endswith('knowledge_book') and reward.get(rid):
            m = re.search(r'loot give @s loot (canon:[\w/]+)', fn_text(reward[rid]))
            if m:
                name = loot_name(m.group(1))
        title = {'text': (name or fn[:-5].replace('_', ' ').capitalize()) + '\n', 'bold': True, 'color': 'dark_red'}
        if not name and res_id and not res_id.endswith('knowledge_book'):
            iid = res_id.split(':')[1]
            title = {'translate': ('block.minecraft.' if iid in blocks else 'item.minecraft.') + iid, 'bold': True, 'color': 'dark_red'}
        body = ['', title]
        if not name and 'translate' in title:
            body.append({'text': '\n'})
        if d.get('type') == 'minecraft:crafting_shaped':
            key = d.get('key', {})
            letters = {k: 'ABCDEFGHI'[i] for i, k in enumerate(sorted(key))}
            for row in d.get('pattern', []):
                body.append({'text': ' '.join(('[' + letters[ch] + ']') if ch in letters else '[  ]' for ch in row) + '\n', 'color': 'dark_gray'})
            body.append({'text': '\n'})
            for k in sorted(key):
                body += [{'text': letters[k] + ' = ', 'bold': True}, comp(key[k]), {'text': '\n'}]
        elif d.get('type') == 'minecraft:crafting_shapeless':
            body.append({'text': 'Sin forma, junta:\n', 'italic': True, 'color': 'dark_gray'})
            for ing in d.get('ingredients', []):
                body += [{'text': '• '}, comp(ing), {'text': '\n'}]
        else:
            continue
        pages.append(json.dumps(body, ensure_ascii=False))
    intro = json.dumps(['', {'text': 'RECETARIO\nCanon Event\n\n', 'bold': True, 'color': 'dark_red'},
                        {'text': 'Todos los crafteos del mod. Al craftear sale un libro raro: no te preocupes, se cambia solo por el ítem de verdad.\n\n'
                                 'En creativo: /trigger dv.items set 1 abre el catálogo de todos los ítems.', 'color': 'black'}], ensure_ascii=False)
    pages = [intro] + pages
    snbt = ','.join("'" + p.replace('\\', '\\\\').replace("'", "\\'") + "'" for p in pages)
    c.json('data/canon/loot_tables/cat/recetario.json', {'type': 'minecraft:generic', 'pools': [{'rolls': 1, 'entries': [{
        'type': 'minecraft:item', 'name': 'minecraft:written_book', 'functions': [{'function': 'minecraft:set_nbt', 'tag':
            '{title:"Recetario de Canon Event",author:"Canon Event",generation:0,pages:[' + snbt + ']}'}]}]}]})
    F('cat/recetario', 'tag @s add dv_recetario\nloot give @s loot canon:cat/recetario')

    # ---------------------------------------------------------------- Juli aparece menos y al azar
    c.patch('juli/player', lambda s: s.replace('dv.juli matches 480.. run', 'dv.juli matches 2400.. if predicate canon:azar/1en80 run')
            .replace('dv.juli matches 300.. if score @s dv.jcd matches ..0 run', 'dv.juli matches 1800.. if score @s dv.jcd matches ..0 if predicate canon:azar/1en80 run'))
    # ---------------------------------------------------------------- el Alto (Slenderman) ataca de verdad
    c.patch('alto/think', lambda s: s.replace('run function canon:x/creep', 'run function canon:x/walk')
            .replace('dv.watch matches 80.. run function canon:alto/lunge', 'dv.watch matches 40.. run function canon:alto/lunge')
            .replace('distance=..1.8] run function canon:alto/catch', 'distance=..2.6] run function canon:alto/catch'))
