"""Personajes con forma REAL de jugador de Minecraft y skins estándar de 64x64.

- paint_skin(cfg, expr) dibuja una skin 64x64 (pixel art) a partir de colores/estilo.
- build_character(prefix, cfg, poses, exprs, out) escribe:
    canon:item/modelo/<prefix>_skin_<expr>.png (una textura por expresión)
    modelos <prefix>_<pose> (cuerpo sin cabeza) y <prefix>_cabeza_<expr> (cabeza + capa de pelo)
  Cuerpo y cabeza separados, compatibles con rig_summon (cuerpo y cabeza) y con los frames.
  Usa la escala de rig 0.9375 (altura de jugador). Cualquier skin real de 64x64 también sirve:
  basta con reemplazar el png.
"""
import json, os, random
from PIL import Image

F = 0.25  # px de skin -> unidades uv (64 px = 16)

# rectángulos de la skin estándar (x, y, w, h) por parte y cara
def box_uv(x, y, w, h, d):
    """Red de una caja de skin con origen (x,y), ancho w, alto h, profundidad d."""
    return {
        'up': (x + d, y, w, d), 'down': (x + d + w, y, w, d),
        'east': (x, y + d, d, h), 'north': (x + d, y + d, w, h),
        'west': (x + d + w, y + d, d, h), 'south': (x + d + w + d, y + d, w, h),
    }


PARTS = {  # nombre: (origen uv, w, h, d, origen uv capa)
    'head': ((0, 0), 8, 8, 8, (32, 0)),
    'body': ((16, 16), 8, 12, 4, (16, 32)),
    'arm_r': ((40, 16), 4, 12, 4, (40, 32)),
    'arm_l': ((32, 48), 4, 12, 4, (48, 48)),
    'leg_r': ((0, 16), 4, 12, 4, (0, 32)),
    'leg_l': ((16, 48), 4, 12, 4, (0, 48)),
}


def uvs(part, layer=False):
    (x, y), w, h, d, (ox, oy) = PARTS[part]
    if layer:
        x, y = ox, oy
    r = box_uv(x, y, w, h, d)
    out = {}
    for f, (a, b, ww, hh) in r.items():
        u = [a * F, b * F, (a + ww) * F, (b + hh) * F]
        if f == 'up':
            u = [u[2], u[3], u[0], u[1]]
        if f == 'down':
            u = [u[0], u[3], u[2], u[1]]
        out[f] = u
    return out


# geometría (unidades de modelo; pies en y=-14; el modelo de cabeza va 1 unidad más abajo)
GEOM = {
    'leg_r': ([8, -14, 6], [12, -2, 10]),
    'leg_l': ([4, -14, 6], [8, -2, 10]),
    'body': ([4, -2, 6], [12, 10, 10]),
    'arm_r': ([12, -2, 6], [16, 10, 10]),
    'arm_l': ([0, -2, 6], [4, 10, 10]),
}
HEAD = ([4, 9, 4], [12, 17, 12])
PIV = {'arm_r': [14, 8, 8], 'arm_l': [2, 8, 8], 'leg_r': [10, -2, 8], 'leg_l': [6, -2, 8]}

POSES = {
    'idle': {},
    'walk_a': {'leg_r': (22.5, 'x'), 'leg_l': (-22.5, 'x'), 'arm_r': (-22.5, 'x'), 'arm_l': (22.5, 'x')},
    'walk_b': {'leg_r': (-22.5, 'x'), 'leg_l': (22.5, 'x'), 'arm_r': (22.5, 'x'), 'arm_l': (-22.5, 'x')},
    'reach': {'arm_r': (45, 'x'), 'arm_l': (45, 'x')},
    'run_a': {'leg_r': (45, 'x'), 'leg_l': (-45, 'x'), 'arm_r': (-45, 'x'), 'arm_l': (45, 'x')},
    'run_b': {'leg_r': (-45, 'x'), 'leg_l': (45, 'x'), 'arm_r': (45, 'x'), 'arm_l': (-45, 'x')},
    'arms_up': {'arm_r': (45, 'z'), 'arm_l': (-45, 'z')},
    'dance_a': {'arm_r': (45, 'z'), 'arm_l': (-22.5, 'z'), 'leg_r': (22.5, 'z')},
    'dance_b': {'arm_r': (22.5, 'z'), 'arm_l': (-45, 'z'), 'leg_l': (-22.5, 'z')},
    'laugh': {'arm_r': (22.5, 'x'), 'arm_l': (22.5, 'x')},
    'offer': {'arm_r': (45, 'x')},
    'point': {'arm_r': (45, 'x'), 'arm_l': (-22.5, 'x')},
    'float': {'leg_r': (22.5, 'x'), 'arm_r': (22.5, 'z'), 'arm_l': (-22.5, 'z')},
    'twist': {'arm_r': (45, 'z'), 'arm_l': (45, 'z'), 'leg_r': (-22.5, 'z')},
    'cover': {'arm_r': (-45, 'x'), 'arm_l': (-45, 'x')},
    'sit': {'leg_r': (-45, 'x'), 'leg_l': (-45, 'x')},
    'brazos': {'arm_r': (-45, 'x'), 'arm_l': (-45, 'x')},
}


SC = 0.9375


def _sc(v, head=False):
    """Escala un punto a altura de jugador: x/z alrededor de 8; y desde los pies (-14) o desde el cuello (cabeza)."""
    x, y, z = v
    by = 7.5 if head else -14
    oy = 9 if head else -14
    return [8 + (x - 8) * SC, by + (y - oy) * SC, 8 + (z - 8) * SC]


def _el(name, frm, to, uv, rot=None, inflate=0.0, head=False):
    frm, to = _sc(frm, head), _sc(to, head)
    if rot:
        rot = (rot[0], rot[1], [round(v, 3) for v in _sc(rot[2], head)])
    f = [round(v - inflate, 3) for v in frm]
    t = [round(v + inflate, 3) for v in to]
    e = {'from': f, 'to': t, 'faces': {k: {'uv': [round(x, 4) for x in v], 'texture': '#0'} for k, v in uv.items()}, 'name': name}
    if rot:
        e['rotation'] = {'angle': rot[0], 'axis': rot[1], 'origin': rot[2]}
    return e


def body_elements(pose):
    P = POSES[pose]
    els = []
    for part, (frm, to) in GEOM.items():
        r = P.get(part)
        rot = (r[0], r[1], PIV[part]) if r else None
        els.append(_el(part, frm, to, uvs(part), rot))
        els.append(_el(part + '_capa', frm, to, uvs(part, True), rot, 0.25))
    return els


def head_elements():
    return [_el('head', *HEAD, uvs('head'), head=True), _el('head_capa', *HEAD, uvs('head', True), None, 0.5, head=True)]


# ------------------------------------------------------------------ pintura de la skin
def _hex(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def _sh(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)


class Skin:
    def __init__(self, seed):
        self.im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        self.p = self.im.load()
        self.rng = random.Random(seed)

    def px(self, x, y, c, noise=0.05):
        if 0 <= x < 64 and 0 <= y < 64:
            self.p[x, y] = _sh(c, 1 + self.rng.uniform(-noise, noise)) if c[3] == 255 else c

    def rect(self, x, y, w, h, c, noise=0.05, shade=True):
        for i in range(w):
            for j in range(h):
                f = 1.0
                if shade and h > 3:
                    f = 1.06 - 0.14 * j / (h - 1)
                self.px(x + i, y + j, _sh(c, f), noise)

    def face_rect(self, part, face, layer=False):
        (x, y), w, h, d, (ox, oy) = PARTS[part]
        if layer:
            x, y = ox, oy
        return box_uv(x, y, w, h, d)[face]

    def fill_box(self, part, c, layer=False, faces=None, noise=0.05):
        for f, (x, y, w, h) in box_uv(*(PARTS[part][4] if layer else PARTS[part][0]), *PARTS[part][1:4]).items():
            if faces and f not in faces:
                continue
            self.rect(x, y, w, h, c, noise)


def paint_skin(cfg, expr='neutral'):
    """cfg: skin, hair, hair_style (short|long|bob|ponytail|bun|emo|bald|messy|braids), eyes, brows, lips,
    top, top_style (tshirt|long|hoodie|blouse|dress|cardigan|jacket|tank), top2 (detalle), pants, pants_style
    (pants|skirt|long_dress|shorts), shoes, extras (lista: necklace, glasses, apron, collar_white, blush, freckles,
    dark_circles, scar, earrings, tie, belt, cap, shawl, makeup), pale_alpha (fantasmas)."""
    S = Skin(sum(map(ord, json.dumps(cfg, sort_keys=True))))
    sk = _hex(cfg['skin'])
    hair = _hex(cfg.get('hair', '#2a1a12'))
    top = _hex(cfg.get('top', '#444444'))
    pants = _hex(cfg.get('pants', '#2b3550'))
    shoes = _hex(cfg.get('shoes', '#222222'))
    ex = set(cfg.get('extras', []))
    # piel base en todo
    for part in ('head', 'body', 'arm_r', 'arm_l', 'leg_r', 'leg_l'):
        S.fill_box(part, sk, noise=0.03)
    # ---------------- ropa
    ts = cfg.get('top_style', 'tshirt')
    sleeve_len = {'tshirt': 4, 'long': 12, 'hoodie': 12, 'blouse': 12, 'dress': 4, 'cardigan': 12, 'jacket': 12, 'tank': 0}.get(ts, 4)
    S.fill_box('body', top)
    for arm in ('arm_r', 'arm_l'):
        for f, (x, y, w, h) in box_uv(*PARTS[arm][0], *PARTS[arm][1:4]).items():
            if f in ('up',):
                if sleeve_len:
                    S.rect(x, y, w, h, top)
            elif f != 'down':
                S.rect(x, y, w, min(h, sleeve_len), top)
                if sleeve_len >= 12:
                    S.rect(x, y + h - 1, w, 1, sk, shade=False)
    t2 = _hex(cfg.get('top2', cfg.get('top', '#444444')))
    bx, by, bw, bh = S.face_rect('body', 'north')
    if ts == 'hoodie':
        S.rect(bx + 2, by + 7, 4, 3, _sh(top, 0.8))
        S.px(bx + 3, by + 1, (230, 230, 230, 255)); S.px(bx + 4, by + 1, (230, 230, 230, 255))
        S.rect(bx + 3, by + 2, 1, 3, (230, 230, 230, 255), shade=False); S.rect(bx + 4, by + 2, 1, 3, (230, 230, 230, 255), shade=False)
        hx, hy, hw, hh = S.face_rect('head', 'south', True)
        S.rect(hx, hy + 5, hw, 3, _sh(top, 0.9))
    if ts in ('cardigan', 'jacket'):
        S.rect(bx + 3, by, 2, bh, t2, shade=False)
        for k in range(2, bh - 1, 3):
            S.px(bx + 3, by + k, (200, 190, 170, 255))
    if ts == 'blouse':
        S.rect(bx, by, 3, 2, sk)
    if ts == 'tank':
        S.rect(bx, by, 2, 2, sk); S.rect(bx + 6, by, 2, 2, sk)
    if 'print' in cfg:
        pc = _hex(cfg['print'])
        S.rect(bx + 2, by + 3, 4, 3, pc, shade=False)
        S.rect(bx + 3, by + 4, 2, 1, top, shade=False)
    # pantalón / falda / vestido
    ps = cfg.get('pants_style', 'pants')
    for leg in ('leg_r', 'leg_l'):
        for f, (x, y, w, h) in box_uv(*PARTS[leg][0], *PARTS[leg][1:4]).items():
            if f == 'down':
                S.rect(x, y, w, h, shoes)
                continue
            if f == 'up':
                S.rect(x, y, w, h, pants)
                continue
            if ps == 'pants':
                S.rect(x, y, w, h - 2, pants)
            elif ps == 'shorts':
                S.rect(x, y, w, 5, pants)
            elif ps in ('skirt', 'long_dress'):
                tights = _hex(cfg.get('tights', cfg['skin']))
                S.rect(x, y, w, h - 2, tights, noise=0.03)
            S.rect(x, y + h - 2, w, 2, shoes)
    if ps in ('skirt', 'long_dress'):
        L = 6 if ps == 'skirt' else 11
        for leg in ('leg_r', 'leg_l'):
            for f, (x, y, w, h) in box_uv(*PARTS[leg][4], *PARTS[leg][1:4]).items():
                if f in ('north', 'south', 'east', 'west'):
                    S.rect(x, y, w, L, pants)
                    for k in range(0, w, 2):
                        S.px(x + k, y + L - 1, _sh(pants, 0.7))
        for f, (x, y, w, h) in box_uv(*PARTS['body'][4], *PARTS['body'][1:4]).items():
            if f in ('north', 'south', 'east', 'west'):
                S.rect(x, y + h - 2, w, 2, pants)
    if 'belt' in ex:
        S.rect(bx, by + bh - 1, bw, 1, (40, 30, 24, 255), shade=False)
    if 'apron' in ex:
        S.rect(bx + 1, by + 4, 6, 8, (236, 232, 222, 255))
    if 'tie' in ex:
        S.rect(bx + 3, by, 2, 7, (120, 20, 24, 255), shade=False)
    if 'collar_white' in ex:
        S.rect(bx + 2, by, 4, 1, (240, 240, 240, 255), shade=False)
    if 'necklace' in ex:
        S.px(bx + 2, by + 1, (220, 220, 228, 255)); S.px(bx + 3, by + 2, (220, 220, 228, 255))
        S.px(bx + 4, by + 2, (220, 220, 228, 255)); S.px(bx + 5, by + 1, (220, 220, 228, 255))
        S.px(bx + 4, by + 3, (250, 250, 255, 255))
    if 'shawl' in ex:
        sc = _hex(cfg.get('shawl', '#6a3a4a'))
        S.rect(bx, by, bw, 4, sc)
        for arm in ('arm_r', 'arm_l'):
            ax, ay, aw, ah = S.face_rect(arm, 'north', True)
            S.rect(ax, ay, aw, 3, sc)
    # ---------------- cabeza
    fx, fy, fw, fh = S.face_rect('head', 'north')
    hs = cfg.get('hair_style', 'short')
    # pelo en la cabeza base (arriba, atrás, lados)
    S.fill_box('head', hair, faces=['up'])
    if hs != 'bald':
        for f in ('south', 'east', 'west'):
            x, y, w, h = S.face_rect('head', f)
            top_rows = {'short': 3, 'emo': 4, 'messy': 4, 'bun': 3, 'long': 8, 'bob': 6, 'ponytail': 4, 'braids': 8}[hs] if f != 'south' else 8
            if hs in ('short', 'emo', 'messy', 'bun', 'ponytail') and f == 'south':
                top_rows = 6
            S.rect(x, y, w, top_rows, hair)
        S.rect(fx, fy, fw, 2 if hs != 'emo' else 2, hair)
    else:
        S.fill_box('head', _hex(cfg.get('hair', '#bdbdbd')), faces=['up'])
    # capa de pelo (overlay)
    lay = {}
    for f in ('north', 'south', 'east', 'west', 'up'):
        lay[f] = S.face_rect('head', f, True)
    if hs in ('long', 'bob', 'braids'):
        x, y, w, h = lay['south']
        S.rect(x, y, w, h, hair)
        for f in ('east', 'west'):
            x, y, w, h = lay[f]
            S.rect(x, y, w, h if hs != 'bob' else 7, hair)
        x, y, w, h = lay['north']
        S.rect(x, y, w, 2, hair)
        S.rect(x, y + 2, 1, h - (1 if hs != 'bob' else 2), hair)
        S.rect(x + w - 1, y + 2, 1, h - (1 if hs != 'bob' else 2), hair)
        x, y, w, h = lay['up']
        S.rect(x, y, w, h, hair)
    if hs == 'emo':
        x, y, w, h = lay['north']
        S.rect(x, y, w, 2, hair)
        S.rect(x + 3, y + 2, 5, 2, hair)
        S.rect(x + 5, y + 4, 3, 1, hair)
    if hs == 'messy':
        x, y, w, h = lay['up']
        for k in range(0, 8, 2):
            S.px(x + k, y + S.rng.randint(0, 7), hair)
    if hs == 'bun':
        x, y, w, h = lay['up']
        S.rect(x + 2, y + 4, 4, 4, _sh(hair, 1.1))
    if hs == 'ponytail':
        x, y, w, h = lay['south']
        S.rect(x + 3, y + 2, 2, 6, hair)
        S.px(x + 3, y + 2, (120, 40, 60, 255)); S.px(x + 4, y + 2, (120, 40, 60, 255))
    # cara
    eye = _hex(cfg.get('eyes', '#3a2618'))
    white = (240, 238, 232, 255)
    brow = _hex(cfg.get('brows', cfg.get('hair', '#2a1a12')))
    lips = _hex(cfg.get('lips', '#a65a55'))
    ey = fy + 4
    l, r = fx + 1, fx + 5
    if expr in ('neutral', 'smile', 'sad', 'angry', 'surprised', 'cry', 'soft', 'laugh', 'scared', 'flat'):
        for x0 in (l, r):
            S.px(x0, ey, white, 0); S.px(x0 + 1, ey, eye, 0)
        if expr == 'scared' or expr == 'surprised':
            for x0 in (l, r):
                S.px(x0, ey - 1, white, 0); S.px(x0 + 1, ey - 1, white, 0)
        if expr in ('soft', 'laugh'):
            for x0 in (l, r):
                S.px(x0, ey, brow, 0); S.px(x0 + 1, ey, brow, 0)
        if expr == 'angry':
            S.px(l, ey - 1, brow, 0); S.px(l + 1, ey - 1, _sh(brow, 1.0), 0); S.px(r, ey - 1, brow, 0); S.px(r + 1, ey - 1, brow, 0)
        else:
            if hs != 'emo':
                S.px(l, ey - 1, brow, 0); S.px(l + 1, ey - 1, brow, 0)
            S.px(r, ey - 1, brow, 0); S.px(r + 1, ey - 1, brow, 0)
    elif expr in ('void', 'creepy', 'glitch'):
        for x0 in (l, r):
            S.px(x0, ey, (8, 8, 8, 255), 0); S.px(x0 + 1, ey, (8, 8, 8, 255), 0)
            S.px(x0, ey + 1, (20, 10, 10, 255), 0)
    elif expr == 'glow':
        for x0 in (l, r):
            S.px(x0, ey, (255, 255, 240, 255), 0); S.px(x0 + 1, ey, (255, 255, 240, 255), 0)
    elif expr == 'red':
        for x0 in (l, r):
            S.px(x0, ey, (230, 200, 200, 255), 0); S.px(x0 + 1, ey, (180, 10, 10, 255), 0)
    if 'dark_circles' in ex and expr not in ('void', 'creepy', 'glitch'):
        for x0 in (l, r):
            S.px(x0, ey + 1, _sh(sk, 0.78), 0); S.px(x0 + 1, ey + 1, _sh(sk, 0.78), 0)
    if 'makeup' in ex:
        for x0 in (l, r):
            S.px(x0, ey - 1, (20, 20, 20, 255), 0)
    if 'blush' in ex and expr not in ('void', 'creepy'):
        S.px(fx + 1, fy + 5, _sh(_hex('#e6a0a0'), 1.0), 0); S.px(fx + 6, fy + 5, _sh(_hex('#e6a0a0'), 1.0), 0)
    if 'freckles' in ex:
        S.px(fx + 2, fy + 5, _sh(sk, 0.8), 0); S.px(fx + 5, fy + 5, _sh(sk, 0.8), 0)
    if 'scar' in ex:
        S.px(fx + 6, fy + 3, (120, 50, 50, 255), 0); S.px(fx + 6, fy + 4, (120, 50, 50, 255), 0)
    if 'glasses' in ex:
        gx, gy = fx, ey
        for x0 in (l - 0, r - 0):
            S.px(x0 - 1 if x0 == l else x0 + 2, gy, (60, 50, 40, 255), 0)
        S.px(fx + 3, gy - 1, (60, 50, 40, 255), 0); S.px(fx + 4, gy - 1, (60, 50, 40, 255), 0)
        S.px(l, gy - 1, (60, 50, 40, 255), 0); S.px(r + 1, gy - 1, (60, 50, 40, 255), 0)
    S.px(fx + 3, fy + 5, _sh(sk, 0.85), 0)
    my = fy + 6
    if expr in ('neutral', 'flat'):
        S.px(fx + 3, my, lips, 0); S.px(fx + 4, my, lips, 0)
    elif expr in ('smile', 'soft'):
        S.px(fx + 2, my, lips, 0); S.px(fx + 3, my + 1 if False else my, lips, 0); S.px(fx + 4, my, lips, 0); S.px(fx + 5, my, lips, 0)
        S.px(fx + 2, my - 1, lips, 0); S.px(fx + 5, my - 1, lips, 0)
    elif expr == 'laugh':
        for k in range(2, 6):
            S.px(fx + k, my, (60, 16, 16, 255), 0)
        S.px(fx + 3, my, (240, 240, 240, 255), 0); S.px(fx + 4, my, (240, 240, 240, 255), 0)
    elif expr in ('sad', 'cry'):
        S.px(fx + 3, my, lips, 0); S.px(fx + 4, my, lips, 0); S.px(fx + 2, my + 1, lips, 0); S.px(fx + 5, my + 1, lips, 0)
        if expr == 'cry':
            S.px(l, ey + 1, (150, 200, 235, 255), 0); S.px(r + 1, ey + 1, (150, 200, 235, 255), 0)
    elif expr in ('surprised', 'scared'):
        S.px(fx + 3, my, (60, 16, 16, 255), 0); S.px(fx + 4, my, (60, 16, 16, 255), 0)
        S.px(fx + 3, my + 1, (60, 16, 16, 255), 0); S.px(fx + 4, my + 1, (60, 16, 16, 255), 0)
    elif expr == 'angry':
        for k in range(2, 6):
            S.px(fx + k, my, _sh(lips, 0.7), 0)
    elif expr in ('creepy', 'glitch', 'glow'):
        for k in range(1, 7):
            S.px(fx + k, my, (235, 230, 215, 255), 0)
        for k in range(1, 7, 2):
            S.px(fx + k, my + 1, (40, 10, 10, 255), 0)
    elif expr == 'void':
        S.px(fx + 3, my, (10, 10, 10, 255), 0); S.px(fx + 4, my, (10, 10, 10, 255), 0)
        S.px(fx + 3, my + 1, (10, 10, 10, 255), 0); S.px(fx + 4, my + 1, (10, 10, 10, 255), 0)
    if 'earrings' in ex:
        x, y, w, h = S.face_rect('head', 'east')
        S.px(x + 4, y + 6, (220, 220, 230, 255), 0)
        x, y, w, h = S.face_rect('head', 'west')
        S.px(x + 3, y + 6, (220, 220, 230, 255), 0)
    if 'cap' in ex:
        cc = _hex(cfg.get('cap', '#1f2b44'))
        for f in ('north', 'south', 'east', 'west'):
            x, y, w, h = lay[f]
            S.rect(x, y, w, 2, cc)
        x, y, w, h = lay['up']
        S.rect(x, y, w, h, cc)
    alpha = cfg.get('alpha')
    if alpha:
        px = S.im.load()
        for i in range(64):
            for j in range(64):
                c = px[i, j]
                if c[3]:
                    px[i, j] = (c[0], c[1], c[2], alpha)
    return S.im


def build_character(prefix, cfg, out, poses=('idle', 'walk_a', 'walk_b', 'reach'), exprs=('neutral', 'smile'), extra_poses=None):
    """Escribe skins y modelos. Devuelve [nombres de modelos de cuerpo (en orden de poses)], [cabezas]."""
    tex_dir = os.path.join(out, 'assets', 'canon', 'textures', 'item', 'modelo')
    mod_dir = os.path.join(out, 'assets', 'canon', 'models', 'modelo')
    os.makedirs(tex_dir, exist_ok=True)
    os.makedirs(mod_dir, exist_ok=True)
    if extra_poses:
        POSES.update(extra_poses)
    exprs = [e if isinstance(e, tuple) else (e, e) for e in exprs]
    base_tex = f'{prefix}_skin'
    paint_skin(cfg, exprs[0][1]).save(os.path.join(tex_dir, base_tex + '.png'))
    bodies = []
    for p in poses:
        m = {'textures': {'0': 'canon:item/modelo/' + base_tex, 'particle': 'canon:item/modelo/' + base_tex},
             'elements': body_elements(p)}
        json.dump(m, open(os.path.join(mod_dir, f'{prefix}_{p}.json'), 'w'), separators=(',', ':'))
        bodies.append(f'{prefix}_{p}')
    heads = []
    for e, pe in exprs:
        tn = f'{prefix}_skin_{e}'
        paint_skin(cfg, pe).save(os.path.join(tex_dir, tn + '.png'))
        m = {'textures': {'0': 'canon:item/modelo/' + tn, 'particle': 'canon:item/modelo/' + tn}, 'elements': head_elements()}
        json.dump(m, open(os.path.join(mod_dir, f'{prefix}_cabeza_{e}.json'), 'w'), separators=(',', ':'))
        heads.append(f'{prefix}_cabeza_{e}')
    return bodies, heads
