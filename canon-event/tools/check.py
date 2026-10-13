"""Verificador de Canon Event (sobre build/out). No reemplaza jugar, pero atrapa
casi todo lo que haría fallar una función al cargar.

1. Sintaxis oficial de comandos con mecha (árbol de comandos 1.20).
2. Nada de 1.20.2+: /return, /random, /tick, macros ($), function ... with,
   execute if function, scoreboard players display, /transfer.
3. Registros 1.20.1 (minecraft-data): bloques + estados, ítems, entidades,
   efectos, partículas, sonidos vanilla, biomas.
4. Referencias internas: funciones, predicados, loot tables, sonidos canon:,
   dimensiones, objetivos de scoreboard, constantes #N dv.math.
5. JSON de tellraw/title/NBT, volumen de /fill, modelos, texturas, ogg.

Uso: python3 tools/check.py [carpeta_out]
"""
import json, os, re, subprocess, sys, tempfile, shutil

TOOLS = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TOOLS, '..', 'build', 'out')
FN = os.path.join(OUT, 'data', 'canon', 'functions')
A = os.path.join(OUT, 'assets')
REG = json.load(open(os.path.join(TOOLS, 'canon', 'registry_1_20_1.json')))
BLOCKS = REG['blocks']
ITEMS = set(REG['items'])
ENTS = set(REG['entities']) | {'canonevent:diana', 'canonevent:gigante', 'diana', 'gigante'}  # entidades Java del mod
EFFECTS = set(REG['effects'])
PARTS = set(REG['particles'])
VSOUNDS = set(REG['sounds'])
BIOMES = set(REG['biomes'])
errors = []


def err(where, msg):
    errors.append(f'{where}: {msg}')


COMMANDS = set('''advancement attribute bossbar clear clone damage data datapack defaultgamemode difficulty effect enchant execute
experience fill fillbiome forceload function gamemode gamerule give help item jfr kick kill list locate loot me msg particle
place playsound recipe reload ride say schedule scoreboard seed setblock setworldspawn spawnpoint spectator spreadplayers
stopsound summon tag team teammsg teleport tell tellraw time title tm tp trigger w weather worldborder xp'''.split())

funcs = {}
for dp, dn, fs in os.walk(FN):
    for f in fs:
        if f.endswith('.mcfunction'):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, FN)[:-len('.mcfunction')].replace(os.sep, '/')
            funcs[rel] = open(p, encoding='utf-8').read()


def exists_data(kind, ident):
    if ident.startswith('#'):
        ns, path = ident[1:].split(':', 1)
        if ns == 'minecraft':
            return True
        return os.path.exists(os.path.join(OUT, 'data', ns, 'tags', kind, path + '.json'))
    ns, path = ident.split(':', 1)
    ext = {'predicates': '.json', 'loot_tables': '.json', 'structures': '.nbt', 'dimension': '.json'}[kind]
    if ns == 'minecraft':
        return True
    return os.path.exists(os.path.join(OUT, 'data', ns, kind, path + ext))


sounds = json.load(open(os.path.join(A, 'canon', 'sounds.json')))
alltext = '\n'.join(funcs.values())
objectives = set(re.findall(r'scoreboard objectives add (\S+)', alltext))
consts = set(re.findall(r'scoreboard players set #(\d+) dv\.math', alltext))
for o in objectives:
    if len(o) > 16:
        err('load', f'objetivo con más de 16 caracteres: {o}')


def balanced(s):
    st = []
    pairs = {')': '(', ']': '[', '}': '{'}
    q = None
    i = 0
    while i < len(s):
        c = s[i]
        if q:
            if c == '\\':
                i += 2
                continue
            if c == q:
                q = None
        else:
            if c in '"\'':
                q = c
            elif c in '([{':
                st.append(c)
            elif c in ')]}':
                if not st or st.pop() != pairs[c]:
                    return False
        i += 1
    return not st and q is None


def split_execute_run(line):
    while line.startswith('execute '):
        idx = line.find(' run ')
        if idx < 0:
            return None
        line = line[idx + 5:]
    return line


def json_after(s):
    s = s.strip()
    try:
        obj, end = json.JSONDecoder().raw_decode(s)
        return obj, s[end:].strip()
    except Exception as e:
        return None, str(e)


def skip_selector(s):
    s = s.lstrip()
    if s.startswith('@'):
        i = 2
        if i < len(s) and s[i] == '[':
            d = 0
            while i < len(s):
                if s[i] == '[':
                    d += 1
                elif s[i] == ']':
                    d -= 1
                    if d == 0:
                        i += 1
                        break
                i += 1
        return s[i:]
    return s[s.find(' '):] if ' ' in s else ''


TEXT_KEYS = {'text', 'color', 'bold', 'italic', 'underlined', 'strikethrough', 'obfuscated', 'font', 'insertion',
             'clickEvent', 'hoverEvent', 'extra', 'score', 'selector', 'translate', 'with', 'keybind', 'nbt', 'block',
             'entity', 'storage', 'interpret', 'separator'}


def check_text_component(w, obj):
    if isinstance(obj, list):
        for o in obj:
            check_text_component(w, o)
    elif isinstance(obj, dict):
        for k in obj:
            if k not in TEXT_KEYS:
                err(w, f'clave desconocida en texto JSON: {k}')
        if 'extra' in obj:
            check_text_component(w, obj['extra'])
        ce = obj.get('clickEvent')
        if ce:
            if ce.get('action') not in ('run_command', 'suggest_command', 'open_url', 'copy_to_clipboard', 'change_page'):
                err(w, 'clickEvent con acción inválida')
            v = ce.get('value', '')
            if ce.get('action') == 'run_command' and v.startswith('/trigger '):
                obj_name = v.split()[1]
                if obj_name not in objectives:
                    err(w, f'trigger sobre objetivo no creado {obj_name}')
            if ce.get('action') in ('run_command', 'suggest_command') and v.startswith('/function canon:'):
                fp = v.split()[1].split(':')[1]
                if fp not in funcs:
                    err(w, f'botón llama función inexistente {fp}')


BLOCK_RE = re.compile(r'(?<![#\w:])(?:minecraft:)?([a-z_]+)(\[[^\]]*\])?(?=[\s{]|$)')


def check_block(w, ident, states):
    if ident.startswith('#'):
        if not exists_data('blocks', ident):
            err(w, f'tag de bloques inexistente {ident}')
        return
    name = ident.split(':')[-1]
    if ident.startswith('canon:'):
        err(w, f'bloque canon: no existe {ident}')
        return
    if name not in BLOCKS:
        err(w, f'bloque inexistente: {ident}')
        return
    if states:
        for kv in states.strip('[]').split(','):
            if not kv.strip():
                continue
            if '=' not in kv:
                err(w, f'estado mal escrito {kv} en {name}')
                continue
            k, v = [x.strip() for x in kv.split('=', 1)]
            if k not in BLOCKS[name]:
                err(w, f'el bloque {name} no tiene la propiedad {k}')
            elif BLOCKS[name][k] and v not in BLOCKS[name][k]:
                err(w, f'valor inválido {k}={v} para {name} (válidos: {BLOCKS[name][k]})')


def block_args(line):
    """Devuelve (id, estados) de los bloques usados en setblock/fill/if block/clone filter."""
    found = []
    toks = re.finditer(r'((?:#?[a-z0-9_]+:)?[a-z0-9_/]+)(\[[^\]]*\])?', line)
    return found


def check_line_registries(w, line):
    # setblock / fill / if|unless block
    for m in re.finditer(r'\b(setblock|if block|unless block)\s+(\S+\s+\S+\s+\S+)\s+((?:#?[a-z0-9_]+:)?[a-z0-9_/]+)(\[[^\]]*\])?', line):
        ident = m.group(3)
        if ':' not in ident and not ident.startswith('#'):
            ident = 'minecraft:' + ident
        check_block(w, ident, m.group(4))
    for m in re.finditer(r'\bfill\s+(\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+)\s+((?:#?[a-z0-9_]+:)?[a-z0-9_/]+)(\[[^\]]*\])?(?:\s+replace\s+((?:#?[a-z0-9_]+:)?[a-z0-9_/]+)(\[[^\]]*\])?)?', line):
        check_block(w, m.group(2) if ':' in m.group(2) else 'minecraft:' + m.group(2), m.group(3))
        if m.group(4):
            check_block(w, m.group(4) if ':' in m.group(4) or m.group(4).startswith('#') else 'minecraft:' + m.group(4), m.group(5))
    for m in re.finditer(r'block_state:\{Name:"([a-z0-9_:]+)"(?:,Properties:\{([^}]*)\})?', line):
        props = None
        if m.group(2):
            props = '[' + ','.join(p.replace(':', '=').replace('"', '') for p in m.group(2).split(',')) + ']'
        check_block(w, m.group(1), props)
    # entidades
    for m in re.finditer(r'\bsummon\s+(?:minecraft:)?((?:canonevent:)?[a-z_]+)', line):
        if m.group(1) not in ENTS:
            err(w, f'entidad inexistente en summon: {m.group(1)}')
    for t in [t for sel in re.findall(r'@[aeprs]\[([^\]]*)\]', line) for t in re.findall(r'(?:^|,)type=!?(#?[a-z0-9_:]+)', sel)]:
        if t.startswith('#'):
            if not exists_data('entity_types', t):
                err(w, f'tag de entidades inexistente {t}')
        elif t.split(':')[-1] not in ENTS:
            err(w, f'tipo de entidad inexistente {t}')
    # ítems
    for m in re.finditer(r'id:"minecraft:([a-z_]+)",Count', line):
        if m.group(1) not in ITEMS:
            err(w, f'ítem inexistente en NBT: {m.group(1)}')
    for m in re.finditer(r'id:"minecraft:([a-z_]+)"(?!,Count)', line):
        if m.group(1) not in ITEMS and m.group(1) not in ENTS:
            err(w, f'id inexistente en NBT: {m.group(1)}')
    for m in re.finditer(r'(?<!effect )(?<!loot )(?<!recipe )\bgive\s+(@\S+)\s+(?:minecraft:)?([a-z_]+)', line):
        if m.group(2) not in ITEMS:
            err(w, f'ítem inexistente en give: {m.group(2)}')
    for m in re.finditer(r'\bwith\s+(?:minecraft:)?([a-z_]+)', line):
        if line.lstrip().startswith('item') or ' run item ' in line:
            if m.group(1) not in ITEMS:
                err(w, f'ítem inexistente en item replace: {m.group(1)}')
    for m in re.finditer(r'(?<!effect )\bclear\s+(@\S+)\s+(?:minecraft:)?([a-z_]+)', line):
        if m.group(2) not in ITEMS:
            err(w, f'ítem inexistente en clear: {m.group(2)}')
    # efectos
    for m in re.finditer(r'\beffect\s+(?:give|clear)\s+\S+\s+(?:minecraft:)?([a-z_]+)', line):
        if m.group(1) not in EFFECTS:
            err(w, f'efecto inexistente: {m.group(1)}')
    # partículas
    for m in re.finditer(r'\bparticle\s+(?:minecraft:)?([a-z_]+)', line):
        if m.group(1) not in PARTS:
            err(w, f'partícula inexistente: {m.group(1)}')
        if m.group(1) in ('block', 'block_marker', 'falling_dust'):
            mm = re.search(r'particle\s+(?:minecraft:)?(?:block|block_marker|falling_dust)\s+(\S+?)(\[[^\]]*\])?\s', line)
            if mm:
                check_block(w, mm.group(1) if ':' in mm.group(1) else 'minecraft:' + mm.group(1), mm.group(2))
    # sonidos vanilla
    for m in re.finditer(r'\b(?:playsound|stopsound\s+\S+\s+\S+)\s+minecraft:([a-z0-9_.]+)', line):
        if m.group(1) not in VSOUNDS:
            err(w, f'sonido vanilla inexistente: {m.group(1)}')


for name, text in funcs.items():
    for n, line in enumerate(text.split('\n'), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        w = f'{name}:{n}'
        if line.startswith('$'):
            err(w, 'macros ($) no existen en 1.20.1')
            continue
        first = line.split(' ', 1)[0]
        if first.startswith('/'):
            err(w, 'empieza con /')
        if first not in COMMANDS:
            err(w, f'comando desconocido o no disponible en 1.20.1: {first}')
        if not balanced(line):
            err(w, 'paréntesis/corchetes/comillas desbalanceados')
        if ' run run ' in line or line.endswith(' run'):
            err(w, 'run vacío')
        for bad in (' run return', ' run random ', ' run tick ', ' if function ', ' unless function ', 'players display ', ' run transfer '):
            if bad in line:
                err(w, f'no existe en 1.20.1: {bad.strip()}')
        if re.search(r'function \S+ with ', line):
            err(w, 'function ... with (macros) no existe en 1.20.1')
        for m in re.finditer(r'(?:function|schedule function) (#?)([a-z0-9_.-]+:[a-z0-9_/.-]+)', line):
            if m.group(1):
                tp = os.path.join(OUT, 'data', m.group(2).split(':')[0], 'tags', 'functions', m.group(2).split(':')[1] + '.json')
                if m.group(2).split(':')[0] != 'minecraft' and not os.path.exists(tp):
                    err(w, f'tag de funciones inexistente #{m.group(2)}')
                continue
            ns, p = m.group(2).split(':')
            if ns == 'canon' and p not in funcs:
                err(w, f'función inexistente {m.group(2)}')
        for m in re.finditer(r'predicate (\S+)', line):
            if not exists_data('predicates', m.group(1)):
                err(w, f'predicado inexistente {m.group(1)}')
        for m in re.finditer(r'loot \S+ (?:@\S+ |\S+ \S+ \S+ )?loot (\S+)', line):
            if not exists_data('loot_tables', m.group(1)):
                err(w, f'loot table inexistente {m.group(1)}')
        for m in re.finditer(r'(?:playsound|stopsound \S+ \S+) (canon:[a-z0-9_.]+)', line):
            if m.group(1).split(':')[1] not in sounds:
                err(w, f'sonido inexistente {m.group(1)}')
        for m in re.finditer(r'(?:execute )?in (canon:\S+)', line):
            d = m.group(1)
            if not exists_data('dimension', d):
                err(w, f'dimensión inexistente {d}')
        for m in re.finditer(r'place template (\S+)', line):
            if not exists_data('structures', m.group(1)):
                err(w, f'estructura inexistente {m.group(1)}')
        for m in re.finditer(r'scoreboard players \S+ \S+ (dv\.[a-z0-9_.]+)', line):
            if m.group(1) not in objectives:
                err(w, f'objetivo no creado {m.group(1)}')
        for m in re.finditer(r'score[s]? \S+ (dv\.[a-z0-9_.]+)', line):
            if m.group(1) not in objectives:
                err(w, f'objetivo no creado {m.group(1)}')
        for m in re.finditer(r'scores=\{([^}]*)\}', line):
            for kv in m.group(1).split(','):
                o = kv.split('=')[0]
                if o not in objectives:
                    err(w, f'objetivo no creado {o}')
        for m in re.finditer(r'#(\d+) dv\.math', line):
            if m.group(1) not in consts:
                err(w, f'constante #{m.group(1)} dv.math no definida')
        for m in re.finditer(r'predicate canon:azar/(\S+)', line):
            pass
        check_line_registries(w, line)
        last = split_execute_run(line)
        if last is None:
            continue
        lf = last.split(' ', 1)[0]
        if lf not in COMMANDS:
            err(w, f'comando final desconocido: {lf}')
        if lf == 'tellraw':
            obj, tail = json_after(skip_selector(last[len('tellraw '):]))
            if obj is None or tail:
                err(w, f'JSON de tellraw inválido: {tail[:80]}')
            else:
                check_text_component(w, obj)
        if lf == 'title':
            rest = skip_selector(last[len('title '):]).strip()
            sub = rest.split(' ', 1)
            if sub[0] in ('title', 'subtitle', 'actionbar'):
                obj, tail = json_after(sub[1])
                if obj is None or tail:
                    err(w, f'JSON de title inválido: {tail[:80]}')
                else:
                    check_text_component(w, obj)
            elif sub[0] == 'times' and len(sub[1].split()) != 3:
                err(w, 'title times necesita 3 números')
        if lf == 'fill':
            nums = last.split()[1:7]
            try:
                a = [int(float(x)) for x in nums]
                vol = (abs(a[3] - a[0]) + 1) * (abs(a[4] - a[1]) + 1) * (abs(a[5] - a[2]) + 1)
                if vol > 32768:
                    err(w, f'fill demasiado grande ({vol})')
            except ValueError:
                pass
        if lf == 'forceload':
            nums = last.split()[2:6]
            try:
                a = [int(float(x)) // 16 for x in nums]
                if len(a) == 4 and (abs(a[2] - a[0]) + 1) * (abs(a[3] - a[1]) + 1) > 256:
                    err(w, 'forceload de más de 256 chunks')
            except ValueError:
                pass
        if lf == 'setblock' and '{' not in last and len(last.split()) > 6:
            err(w, 'setblock con argumentos de más')
        if lf == 'damage' and not re.match(r'damage @\S+ \d+(\.\d+)? [a-z0-9_]+:[a-z0-9_/]+( by @\S+)?( from @\S+)?$', last):
            err(w, f'damage con sintaxis rara: {last[:80]}')
        for m in re.finditer(r"(?:text|CustomName|Name|Lore:\[|,)\s*:?'(\{[^']*\}|\[[^']*\])'", line):
            try:
                obj = json.loads(m.group(1))
                check_text_component(w, obj)
            except Exception:
                err(w, f'JSON dentro de NBT inválido: {m.group(1)[:60]}')
        if 'positioned over ' in line:
            hm = line.split('positioned over ')[1].split()[0]
            if hm not in ('world_surface', 'motion_blocking', 'motion_blocking_no_leaves', 'ocean_floor'):
                err(w, f'heightmap inválido {hm}')

# ---------------- datos JSON
for dp, dn, fs in os.walk(os.path.join(OUT, 'data')):
    for f in fs:
        if not f.endswith('.json'):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, OUT)
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            err(rel, 'JSON inválido ' + str(e))
            continue
        s = json.dumps(d)
        for m in re.finditer(r'"(?:name|item)": "minecraft:([a-z_]+)"', s):
            if '/loot_tables/' in p.replace(os.sep, '/') or '/recipes/' in p.replace(os.sep, '/'):
                if m.group(1) not in ITEMS:
                    err(rel, f'ítem inexistente {m.group(1)}')
        for m in re.finditer(r'"items": \[([^\]]*)\]', s):
            for it in re.findall(r'"minecraft:([a-z_]+)"', m.group(1)):
                if it not in ITEMS:
                    err(rel, f'ítem inexistente {it}')
        for m in re.finditer(r'"biome": "minecraft:([a-z_]+)"', s):
            if m.group(1) not in BIOMES:
                err(rel, f'bioma inexistente {m.group(1)}')
        for m in re.finditer(r'"function": "canon:([a-z0-9_/]+)"', s):
            if '/advancements/' in p.replace(os.sep, '/') and m.group(1) not in funcs:
                err(rel, f'recompensa llama función inexistente {m.group(1)}')
        if '/advancements/' in p.replace(os.sep, '/'):
            fn = d.get('rewards', {}).get('function')
            if fn and fn.split(':')[1] not in funcs:
                err(rel, f'recompensa con función inexistente {fn}')
            par = d.get('parent')
            if par and par.startswith('canon:'):
                pp = os.path.join(OUT, 'data', 'canon', 'advancements', par.split(':')[1] + '.json')
                if not os.path.exists(pp):
                    err(rel, f'logro padre inexistente {par}')
        if '/recipes/' in p.replace(os.sep, '/'):
            if d.get('type') not in ('minecraft:crafting_shaped', 'minecraft:crafting_shapeless', 'minecraft:smelting',
                                     'minecraft:stonecutting', 'minecraft:smithing_transform', 'minecraft:campfire_cooking',
                                     'minecraft:smoking', 'minecraft:blasting'):
                err(rel, f'tipo de receta raro {d.get("type")}')
            r = d.get('result', {})
            if isinstance(r, dict) and ('tag' in r or 'components' in r):
                err(rel, 'en Forge 1.20.1 el NBT del resultado va en "nbt"')
for dp, dn, fs in os.walk(A):
    for f in fs:
        if f.endswith('.json'):
            try:
                json.load(open(os.path.join(dp, f), encoding='utf-8'))
            except Exception as e:
                err(os.path.join(dp, f), 'JSON inválido ' + str(e))
# funciones de tags (load/tick)
for tf in ('load', 'tick'):
    p = os.path.join(OUT, 'data', 'minecraft', 'tags', 'functions', tf + '.json')
    for v in json.load(open(p))['values']:
        if v.split(':')[1] not in funcs:
            err(p, f'función inexistente {v}')

# ---------------- modelos y texturas
for ov_file in os.listdir(os.path.join(A, 'minecraft', 'models', 'item')):
    d = json.load(open(os.path.join(A, 'minecraft', 'models', 'item', ov_file)))
    if ov_file[:-5] not in ITEMS:
        err(ov_file, 'modelo para un ítem que no existe')
    seen = set()
    for o in d.get('overrides', []):
        cmd = o['predicate'].get('custom_model_data')
        if cmd in seen:
            err(ov_file, f'CMD repetido {cmd}')
        seen.add(cmd)
        ns, p = o['model'].split(':')
        mp = os.path.join(A, ns, 'models', p + '.json')
        if not os.path.exists(mp):
            err(ov_file, f'modelo inexistente {o["model"]}')
            continue
        m = json.load(open(mp))
        for k, t in m.get('textures', {}).items():
            if t.startswith('#'):
                continue
            tns, tp = t.split(':') if ':' in t else ('minecraft', t)
            if tns != 'minecraft' and not os.path.exists(os.path.join(A, tns, 'textures', tp + '.png')):
                err(mp, f'textura inexistente {t}')
        if 'parent' in m and m['parent'].startswith('canon:'):
            pp = os.path.join(A, 'canon', 'models', m['parent'].split(':')[1] + '.json')
            if not os.path.exists(pp):
                err(mp, f'parent inexistente {m["parent"]}')
        for e in m.get('elements', []):
            for v in e['from'] + e['to']:
                if v < -16 or v > 32:
                    err(mp, f'coordenada fuera de rango {v} en {e.get("name")}')
            r = e.get('rotation')
            if r and (r['angle'] not in (-45, -22.5, 0, 22.5, 45) or r['axis'] not in 'xyz'):
                err(mp, f'rotación inválida {r}')
            for fc in e['faces'].values():
                uv = fc.get('uv')
                if uv and any(u < 0 or u > 16 for u in uv):
                    err(mp, f'uv fuera de rango {uv}')
                if 'texture' in fc and fc['texture'].startswith('#') and fc['texture'][1:] not in m.get('textures', {}):
                    err(mp, f'cara usa textura no declarada {fc["texture"]}')

# ---------------- sonidos
for k, v in sounds.items():
    for s in v['sounds']:
        n = s if isinstance(s, str) else s['name']
        if isinstance(s, dict) and s.get('type') == 'event':
            en = n.split(':')[-1]
            if n.startswith('canon:'):
                if en not in sounds:
                    err('sounds.json', f'{k}: evento canon inexistente {n}')
            elif en not in VSOUNDS:
                err('sounds.json', f'{k}: evento vanilla inexistente {n}')
            continue
        if ':' not in n:
            continue  # sonido vanilla (ruta de archivo)
        ns, p = n.split(':')
        if not os.path.exists(os.path.join(A, ns, 'sounds', p + '.ogg')):
            err('sounds.json', f'ogg inexistente {n}')
    sub = v.get('subtitle')
    if sub:
        lj = json.load(open(os.path.join(A, 'canon', 'lang', 'es_es.json'), encoding='utf-8'))
        if sub not in lj:
            err('sounds.json', f'subtítulo sin traducción en es_es: {sub}')

# ---------------- mecha (sintaxis oficial)
if '--no-mecha' not in sys.argv:
    tmp = tempfile.mkdtemp()
    try:
        shutil.copytree(os.path.join(OUT, 'data'), os.path.join(tmp, 'data'))
        shutil.copy(os.path.join(OUT, 'pack.mcmeta'), tmp)
        r = subprocess.run([sys.executable, '-m', 'mecha', '-m', '1.20', tmp], capture_output=True, text=True)
        outtxt = r.stdout + r.stderr
        for blk in re.split(r'\n(?=ERROR)', outtxt):
            if blk.startswith('ERROR'):
                err('mecha', ' '.join(blk.split('\n')[:2]).replace(tmp, ''))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

for e in errors:
    print(e)
print(f'{len(funcs)} funciones revisadas, {len(errors)} problemas')
sys.exit(1 if errors else 0)
