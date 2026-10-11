"""Verificador estático de Canon Event (no reemplaza probar en el juego).

Revisa en TODO el mod:
- funciones / predicados / loot tables / sonidos / dimensiones referenciados existen
- JSON de tellraw / title / nombres válido
- llaves y corchetes balanceados, comandos conocidos
- volumen de /fill <= 32768
- objetivos de scoreboard usados están creados en load
- modelos: rotaciones válidas, coordenadas dentro de -16..32, texturas existentes
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(__file__), '..', 'src')
FN = os.path.join(ROOT, 'data', 'canon', 'functions')
errors = []


def err(where, msg):
    errors.append(f'{where}: {msg}')


COMMANDS = set('''advancement attribute bossbar clear clone damage data datapack defaultgamemode difficulty effect enchant execute
experience fill fillbiome forceload function gamemode gamerule give help item jfr kick kill list locate loot me msg particle
place playsound recipe reload return ride say schedule scoreboard seed setblock setworldspawn spawnpoint spectator spreadplayers
stopsound summon tag team teammsg teleport tell tellraw time title tm tp trigger w weather worldborder xp'''.split())
# 'return' no existe en 1.20.1
NOT_IN_1201 = {'return', 'random'}

funcs = {}
for dp, dn, fs in os.walk(FN):
    for f in fs:
        if f.endswith('.mcfunction'):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, FN)[:-len('.mcfunction')].replace(os.sep, '/')
            funcs[rel] = open(p, encoding='utf-8').read()


def exists_data(kind, ident):
    ns, path = ident.split(':', 1)
    ext = {'predicates': '.json', 'loot_tables': '.json', 'structures': '.nbt', 'dimension': '.json'}[kind]
    if ns == 'minecraft':
        return True
    return os.path.exists(os.path.join(ROOT, 'data', ns, kind, path + ext))


sounds = json.load(open(os.path.join(ROOT, 'assets', 'canon', 'sounds.json')))

objectives = set(re.findall(r'scoreboard objectives add (\S+)', ''.join(funcs.values())))
objectives |= set()


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
    """devuelve el comando final de una cadena execute ... run X"""
    while line.startswith('execute '):
        idx = line.find(' run ')
        if idx < 0:
            return None
        line = line[idx + 5:]
    return line


def json_after(line, start):
    s = line[start:].strip()
    try:
        dec = json.JSONDecoder()
        obj, end = dec.raw_decode(s)
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


for name, text in funcs.items():
    for n, line in enumerate(text.split('\n'), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        w = f'{name}:{n}'
        first = line.split(' ', 1)[0]
        if first.startswith('/'):
            err(w, 'empieza con /')
        if first not in COMMANDS or first in NOT_IN_1201:
            err(w, f'comando desconocido o no disponible en 1.20.1: {first}')
        if not balanced(line):
            err(w, 'paréntesis/corchetes/comillas desbalanceados')
        if ' run run ' in line or line.endswith(' run'):
            err(w, 'run vacío')
        for m in re.finditer(r'(?:function|schedule function) (#?)([a-z0-9_.-]+:[a-z0-9_/.-]+)', line):
            if m.group(1):
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
        for m in re.finditer(r'execute in (\S+)', line):
            d = m.group(1)
            if d.startswith('canon:') and not exists_data('dimension', d):
                err(w, f'dimensión inexistente {d}')
        for m in re.finditer(r'scoreboard players \S+ \S+ (dv\.[a-z0-9_]+)', line):
            if m.group(1) not in objectives:
                err(w, f'objetivo no creado {m.group(1)}')
        for m in re.finditer(r'score[s]? \S+ (dv\.[a-z0-9_]+)', line):
            if m.group(1) not in objectives:
                err(w, f'objetivo no creado {m.group(1)}')
        for m in re.finditer(r'scores=\{(dv\.[a-z0-9_]+)', line):
            if m.group(1) not in objectives:
                err(w, f'objetivo no creado {m.group(1)}')
        for m in re.finditer(r'#(\d+) dv\.math', line):
            if f'#{m.group(1)} dv.math' not in funcs['load'] and f'#{m.group(1)} dv.math' not in funcs.get('extra/load', ''):
                err(w, f'constante #{m.group(1)} dv.math no definida')
        last = split_execute_run(line)
        if last is None:
            if first == 'execute':
                pass
            continue
        lf = last.split(' ', 1)[0]
        if lf not in COMMANDS or lf in NOT_IN_1201:
            err(w, f'comando final desconocido: {lf}')
        if lf == 'tellraw':
            rest = skip_selector(last[len('tellraw '):])
            obj, tail = json_after(rest, 0)
            if obj is None or tail:
                err(w, f'JSON de tellraw inválido: {tail[:80]}')
        if lf == 'title':
            parts = last.split(' ', 3)
            rest = skip_selector(last[len('title '):]).strip()
            sub = rest.split(' ', 1)
            if sub[0] in ('title', 'subtitle', 'actionbar'):
                obj, tail = json_after(sub[1], 0)
                if obj is None or tail:
                    err(w, f'JSON de title inválido: {tail[:80]}')
            elif sub[0] == 'times':
                if len(sub[1].split()) != 3:
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
        if lf == 'setblock' and '{' not in last and len(last.split()) > 6:
            err(w, 'setblock con argumentos de más')
        if lf == 'damage':
            if not re.match(r'damage @\S+ \d+(\.\d+)? [a-z0-9_]+:[a-z0-9_/]+( by @\S+)?$', last):
                err(w, f'damage con sintaxis rara: {last}')
        # SNBT con JSON entre comillas simples
        for m in re.finditer(r"(?:text|CustomName):'([^']*)'", line):
            try:
                json.loads(m.group(1))
            except Exception as e:
                err(w, f'JSON dentro de NBT inválido: {m.group(1)[:60]}')
        if 'positioned over ' in line:
            hm = line.split('positioned over ')[1].split()[0]
            if hm not in ('world_surface', 'motion_blocking', 'motion_blocking_no_leaves', 'ocean_floor'):
                err(w, f'heightmap inválido {hm}')

# ---------------- JSON de datos
for dp, dn, fs in os.walk(os.path.join(ROOT, 'data')):
    for f in fs:
        if f.endswith('.json'):
            try:
                json.load(open(os.path.join(dp, f), encoding='utf-8'))
            except Exception as e:
                err(os.path.join(dp, f), 'JSON inválido ' + str(e))
for dp, dn, fs in os.walk(os.path.join(ROOT, 'assets')):
    for f in fs:
        if f.endswith('.json'):
            try:
                json.load(open(os.path.join(dp, f), encoding='utf-8'))
            except Exception as e:
                err(os.path.join(dp, f), 'JSON inválido ' + str(e))

# ---------------- modelos
A = os.path.join(ROOT, 'assets')
for ov_file in os.listdir(os.path.join(A, 'minecraft', 'models', 'item')):
    d = json.load(open(os.path.join(A, 'minecraft', 'models', 'item', ov_file)))
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
            if ':' in t:
                tns, tp = t.split(':')
                if not os.path.exists(os.path.join(A, tns, 'textures', tp + '.png')):
                    err(mp, f'textura inexistente {t}')
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

# ---------------- sonidos
for k, v in sounds.items():
    for s in v['sounds']:
        n = s if isinstance(s, str) else s['name']
        if ':' not in n:
            continue  # sonido vanilla
        ns, p = n.split(':')
        if not os.path.exists(os.path.join(A, ns, 'sounds', p + '.ogg')):
            err('sounds.json', f'ogg inexistente {n}')

for e in errors:
    print(e)
print(f'{len(funcs)} funciones revisadas, {len(errors)} problemas')
sys.exit(1 if errors else 0)
