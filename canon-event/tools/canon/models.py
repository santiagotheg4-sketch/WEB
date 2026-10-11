"""Librería de modelos 3D (item models con elementos) y texturas pixel-art.

Uso desde un módulo:
    from canon import models as M
    at = M.Atlas('kevin', seed=11)            # textura canon:item/modelo/kevin (256x256)
    P = M.humanoid_parts(at, colores)         # partes del cuerpo
    M.write_model('kevin_idle', 'kevin', M.pose(P, 'idle'))
    at.save()
Las rutas de salida las fija build.py con M.set_out(out).
"""
import json, os, random
from PIL import Image, ImageDraw

OUT = None
SZ = 256
PX = SZ / 16.0


def set_out(out):
    global OUT
    OUT = out


def models_dir():
    p = os.path.join(OUT, 'assets', 'canon', 'models', 'modelo')
    os.makedirs(p, exist_ok=True)
    return p


def tex_dir():
    p = os.path.join(OUT, 'assets', 'canon', 'textures', 'item', 'modelo')
    os.makedirs(p, exist_ok=True)
    return p


def hexc(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (255,)


class Atlas:
    def __init__(self, name, seed=1):
        self.name = name
        self.img = Image.new('RGBA', (SZ, SZ), (0, 0, 0, 0))
        self.x = 0
        self.y = 0
        self.row = 0
        self.rng = random.Random(seed)
        self.cache = {}

    def alloc(self, w, h):
        w = max(2, int(round(w)))
        h = max(2, int(round(h)))
        if self.x + w > SZ:
            self.x = 0
            self.y += self.row
            self.row = 0
        if self.y + h > SZ:
            raise RuntimeError('atlas lleno: ' + self.name)
        r = (self.x, self.y, w, h)
        self.x += w
        self.row = max(self.row, h)
        return r

    def fill(self, r, color, noise=0.06, pattern=None, shading=True):
        """Rellena con ruido + volumen: más claro arriba, más oscuro abajo y borde suave."""
        x, y, w, h = r
        d = ImageDraw.Draw(self.img)
        for i in range(w):
            for j in range(h):
                f = 1 + self.rng.uniform(-noise, noise)
                if shading:
                    if h > 3:
                        f *= 1.07 - 0.16 * (j / (h - 1))
                    if (i == 0 or i == w - 1 or j == h - 1) and w > 3 and h > 3:
                        f *= 0.86
                c = color
                if pattern:
                    c = pattern(i, j, w, h, color) or color
                d.point((x + i, y + j), shade(c, f))

    def uv(self, r):
        x, y, w, h = r
        return [round(x / PX, 4), round(y / PX, 4), round((x + w) / PX, 4), round((y + h) / PX, 4)]

    def save(self):
        self.img.save(os.path.join(tex_dir(), self.name + '.png'))


FACES = ['north', 'south', 'east', 'west', 'up', 'down']


def face_dims(frm, to, f):
    dx, dy, dz = (abs(to[i] - frm[i]) for i in range(3))
    if f in ('north', 'south'):
        return dx, dy
    if f in ('east', 'west'):
        return dz, dy
    return dx, dz


class Part:
    """Una caja con textura propia (se pinta una vez y se reutiliza en todas las poses)."""

    def __init__(self, atlas, name, frm, to, color, faces=None, paint=None, scale=4.0, noise=0.06):
        self.name, self.frm, self.to = name, list(frm), list(to)
        self.uvs = {}
        faces = faces or FACES
        for f in faces:
            w, h = face_dims(frm, to, f)
            r = atlas.alloc(w * scale, h * scale)
            c = color[f] if isinstance(color, dict) else color
            atlas.fill(r, hexc(c) if isinstance(c, str) else c, noise=noise)
            if paint:
                paint(atlas, f, r)
            self.uvs[f] = atlas.uv(r)

    def element(self, rot=None, frm=None, to=None):
        e = {'from': frm or self.frm, 'to': to or self.to,
             'faces': {f: {'uv': uv, 'texture': '#0'} for f, uv in self.uvs.items()},
             'name': self.name}
        if rot:
            e['rotation'] = {'angle': rot[0], 'axis': rot[1], 'origin': rot[2]}
        return e


def write_model(name, tex, elements):
    m = {'textures': {'0': 'canon:item/modelo/' + tex, 'particle': 'canon:item/modelo/' + tex},
         'elements': elements}
    with open(os.path.join(models_dir(), name + '.json'), 'w') as fh:
        json.dump(m, fh, separators=(',', ':'))


# ---------------------------------------------------------------- pintores

def px(atlas, x, y, c):
    if 0 <= x < SZ and 0 <= y < SZ:
        atlas.img.putpixel((x, y), hexc(c) if isinstance(c, str) else c)


def rect(atlas, x, y, w, h, c):
    for i in range(w):
        for j in range(h):
            px(atlas, x + i, y + j, c)


def stripes_v(color2, every=4):
    def p(i, j, w, h, c):
        return hexc(color2) if i % every == 0 else None
    return p


def hair_strands(atlas, f, r):
    x, y, w, h = r
    for i in range(w):
        if atlas.rng.random() < 0.35:
            for j in range(h):
                c = atlas.img.getpixel((x + i, y + j))
                atlas.img.putpixel((x + i, y + j), shade(c, 0.8))


def draw_face(atlas, r, style):
    """Dibuja una cara en un rectángulo (24x26 px aprox: 6x6.4 unidades * 4)."""
    x, y, w, h = r
    s = style
    eye_y = y + int(h * 0.45)
    lx, rx = x + int(w * 0.22), x + int(w * 0.62)
    ew = max(3, int(w * 0.17))
    kind = s.get('eyes', 'normal')
    if kind == 'normal':
        for ex in (lx, rx):
            rect(atlas, ex, eye_y, ew, 2, '#f4f1ec')
            rect(atlas, ex + ew // 2 - 1, eye_y, 2, 2, s.get('iris', '#2b1d14'))
            rect(atlas, ex - 1, eye_y - 2, ew + 2, 1, s.get('brow', '#1c1410'))
    elif kind == 'closed':
        for ex in (lx, rx):
            rect(atlas, ex, eye_y + 1, ew, 1, '#1c1410')
            px(atlas, ex, eye_y, '#1c1410'); px(atlas, ex + ew - 1, eye_y, '#1c1410')
    elif kind == 'red':
        for ex in (lx, rx):
            rect(atlas, ex, eye_y, ew, 2, '#e9b3b3')
            rect(atlas, ex + ew // 2 - 1, eye_y, 2, 2, '#b01212')
            rect(atlas, ex - 1, eye_y + 2, ew + 2, 1, '#6b3a4a')
    elif kind == 'wide':
        for ex in (lx, rx):
            rect(atlas, ex - 1, eye_y - 1, ew + 2, 3, '#ffffff')
            px(atlas, ex + ew // 2, eye_y, '#111111')
            rect(atlas, ex - 1, eye_y - 3, ew + 2, 1, s.get('brow', '#1c1410'))
    elif kind == 'angry':
        for k, ex in enumerate((lx, rx)):
            rect(atlas, ex, eye_y, ew, 2, '#f0e8e0')
            rect(atlas, ex + ew // 2 - 1, eye_y, 2, 2, '#1a1010')
            for t in range(ew + 1):
                yy = eye_y - 3 + (t * 2 // (ew + 1) if k == 0 else 2 - t * 2 // (ew + 1))
                px(atlas, ex - 1 + t, yy, '#0d0d0d')
    elif kind == 'void':
        for ex in (lx, rx):
            rect(atlas, ex - 1, eye_y - 1, ew + 2, 4, '#050505')
            px(atlas, ex + ew // 2, eye_y + 1, '#f6f6f6')
    elif kind == 'glow':
        for ex in (lx, rx):
            rect(atlas, ex - 1, eye_y - 2, ew + 2, 5, '#fbfbf0')
            rect(atlas, ex + ew // 2 - 1, eye_y, 1, 1, '#000000')
    # flequillo emo: tapa un ojo
    if s.get('emo_fringe'):
        rect(atlas, x, y, int(w * 0.62), int(h * 0.5), s['hair'])
        for i in range(int(w * 0.62)):
            if atlas.rng.random() < 0.4:
                px(atlas, x + i, y + int(h * 0.5), s['hair'])
    if s.get('blush'):
        rect(atlas, lx - 1, eye_y + 4, 3, 2, s['blush'])
        rect(atlas, rx + ew - 2, eye_y + 4, 3, 2, s['blush'])
    my = y + int(h * 0.75)
    mx = x + w // 2
    mouth = s.get('mouth', 'smile')
    mc = s.get('lips', '#8a4a44')
    if mouth == 'smile':
        rect(atlas, mx - 3, my, 6, 1, mc); px(atlas, mx - 4, my - 1, mc); px(atlas, mx + 3, my - 1, mc)
    elif mouth == 'flat':
        rect(atlas, mx - 2, my, 4, 1, mc)
    elif mouth == 'open':
        rect(atlas, mx - 2, my - 1, 5, 3, '#3a0e0e'); rect(atlas, mx - 2, my - 1, 5, 1, '#f2f2f2')
    elif mouth == 'laugh':
        rect(atlas, mx - 4, my - 1, 8, 3, '#3a0e0e'); rect(atlas, mx - 4, my - 1, 8, 1, '#f5f5f5')
        rect(atlas, mx - 2, my + 1, 4, 1, '#c25a5a')
    elif mouth == 'scream':
        rect(atlas, mx - 3, my - 3, 6, 6, '#1a0404'); rect(atlas, mx - 3, my - 3, 6, 1, '#e8e2d0')
    elif mouth == 'grin':
        rect(atlas, mx - 6, my - 1, 12, 2, '#efe9d9')
        for t in range(0, 12, 2):
            px(atlas, mx - 6 + t, my, '#2a1010')
        rect(atlas, mx - 7, my - 2, 14, 1, '#2a1010')
    elif mouth == 'frown':
        rect(atlas, mx - 3, my, 6, 1, mc); px(atlas, mx - 4, my + 1, mc); px(atlas, mx + 3, my + 1, mc)
    elif mouth == 'o':
        rect(atlas, mx - 1, my - 1, 3, 3, '#5a1c22')
    elif mouth == 'none':
        pass
    if s.get('tears'):
        for ex in (lx, rx):
            rect(atlas, ex + 1, eye_y + 2, 1, 4, '#9cc7e6')
    if s.get('nose', True) and mouth not in ('none',):
        px(atlas, mx, eye_y + 3, shade(hexc(s['skin']), 0.82))


# ---------------------------------------------------------------- humanoides

ARM_O_R = [12.6, 7, 8]
ARM_O_L = [3.3, 7, 8]
LEG_O = [8, -1, 8]


def humanoid_parts(at, c, build='normal'):
    """c: colores. build: normal | chubby | thin | girl"""
    P = {}
    if build == 'chubby':
        P['leg_r'] = Part(at, 'leg_r', [8.1, -12.4, 6.4], [11.3, -1.2, 9.6], c['pants'])
        P['leg_l'] = Part(at, 'leg_l', [4.7, -12.4, 6.4], [7.9, -1.2, 9.6], c['pants'])
        P['shoe_r'] = Part(at, 'shoe_r', [8, -14, 5.6], [11.4, -12.4, 9.8], c['shoes'])
        P['shoe_l'] = Part(at, 'shoe_l', [4.6, -14, 5.6], [8, -12.4, 9.8], c['shoes'])
        P['hips'] = Part(at, 'hips', [3.9, -1.6, 5.6], [12.1, 0.6, 10.4], c['belt'])
        P['top'] = Part(at, 'top', [3.6, 0.2, 5.2], [12.4, 7.6, 10.8], c['shirt'], paint=c.get('shirt_paint'))
        P['belly'] = Part(at, 'belly', [4.4, 0.6, 4.6], [11.6, 5.4, 5.2], c['shirt'], faces=['north', 'east', 'west', 'down', 'up'])
        P['neck'] = Part(at, 'neck', [7, 7.6, 7], [9, 9, 9], c['skin'])
        P['arm_r'] = Part(at, 'arm_r', [12.4, -1.0, 6.6], [14.8, 7.6, 9.4], c['sleeve'], paint=c.get('arm_paint'))
        P['arm_l'] = Part(at, 'arm_l', [1.2, -1.0, 6.6], [3.6, 7.6, 9.4], c['sleeve'], paint=c.get('arm_paint'))
        return P
    if build == 'thin':
        P['leg_r'] = Part(at, 'leg_r', [8.4, -12.8, 7.0], [10.2, -0.2, 9.0], c['pants'])
        P['leg_l'] = Part(at, 'leg_l', [5.8, -12.8, 7.0], [7.6, -0.2, 9.0], c['pants'])
        P['shoe_r'] = Part(at, 'shoe_r', [8.3, -14, 6.2], [10.3, -12.4, 9.2], c['shoes'])
        P['shoe_l'] = Part(at, 'shoe_l', [5.7, -14, 6.2], [7.7, -12.4, 9.2], c['shoes'])
        P['hips'] = Part(at, 'hips', [5.4, -1.2, 6.8], [10.6, 0.6, 9.2], c['belt'])
        P['top'] = Part(at, 'top', [5.2, 0.2, 6.8], [10.8, 7.6, 9.2], c['shirt'], paint=c.get('shirt_paint'))
        P['neck'] = Part(at, 'neck', [7.3, 7.6, 7.3], [8.7, 9.4, 8.7], c['skin'])
        P['arm_r'] = Part(at, 'arm_r', [10.9, -6.0, 7.2], [12.3, 7.6, 8.8], c['sleeve'], paint=c.get('arm_paint'))
        P['arm_l'] = Part(at, 'arm_l', [3.7, -6.0, 7.2], [5.1, 7.6, 8.8], c['sleeve'], paint=c.get('arm_paint'))
        return P
    leg_top = -0.2
    P['leg_r'] = Part(at, 'leg_r', [8.2, -12.8, 6.65], [10.9, leg_top, 9.35], c['pants'], paint=c.get('leg_paint'))
    P['leg_l'] = Part(at, 'leg_l', [5.1, -12.8, 6.65], [7.8, leg_top, 9.35], c['pants'], paint=c.get('leg_paint'))
    if c.get('boots'):
        P['shoe_r'] = Part(at, 'shoe_r', [8, -14, 5.9], [11.1, -8.6, 9.6], c['shoes'])
        P['shoe_l'] = Part(at, 'shoe_l', [4.9, -14, 5.9], [8, -8.6, 9.6], c['shoes'])
    else:
        P['shoe_r'] = Part(at, 'shoe_r', [8, -14, 5.75], [11.1, -12.4, 9.6], c['shoes'], paint=c.get('shoe_paint'))
        P['shoe_l'] = Part(at, 'shoe_l', [4.9, -14, 5.75], [8, -12.4, 9.6], c['shoes'], paint=c.get('shoe_paint'))
    P['hips'] = Part(at, 'hips', [4.2, -1.4, 6], [11.8, 0.6, 10], c['belt'])
    if c.get('skirt'):
        P['skirt'] = Part(at, 'skirt', [3.8, -5.6, 5.4], [12.2, 0.2, 10.6], c['skirt'],
                          faces=['north', 'south', 'east', 'west', 'down'], paint=c.get('skirt_paint'))
    wide = c.get('wide_shoulders', 0)
    P['top'] = Part(at, 'top', [4.4 - wide, 0.2, 6.2], [11.6 + wide, 7.6, 9.8], c['shirt'], paint=c.get('shirt_paint'))
    P['neck'] = Part(at, 'neck', [7, 7.6, 7], [9, 9, 9], c['skin'])
    aw = c.get('arm_w', 2.1)
    P['arm_r'] = Part(at, 'arm_r', [11.6 + wide, -1.4, 7], [11.6 + wide + aw, 7.6, 9], c['sleeve'], paint=c.get('arm_paint'))
    P['arm_l'] = Part(at, 'arm_l', [4.4 - wide - aw, -1.4, 7], [4.4 - wide, 7.6, 9], c['sleeve'], paint=c.get('arm_paint'))
    return P


def pose(P, name, extra=None):
    """Devuelve elementos de la pose. extra: dict parte -> rotación (angle, axis, origin)."""
    rots = {
        'idle': {},
        'walk_a': {'leg_r': (22.5, 'x', LEG_O), 'shoe_r': (22.5, 'x', LEG_O), 'leg_l': (-22.5, 'x', LEG_O),
                   'shoe_l': (-22.5, 'x', LEG_O), 'arm_r': (-22.5, 'x', ARM_O_R), 'arm_l': (22.5, 'x', ARM_O_L)},
        'walk_b': {'leg_r': (-22.5, 'x', LEG_O), 'shoe_r': (-22.5, 'x', LEG_O), 'leg_l': (22.5, 'x', LEG_O),
                   'shoe_l': (22.5, 'x', LEG_O), 'arm_r': (22.5, 'x', ARM_O_R), 'arm_l': (-22.5, 'x', ARM_O_L)},
        'reach': {'arm_r': (45, 'x', ARM_O_R), 'arm_l': (45, 'x', ARM_O_L)},
        'arms_up': {'arm_r': (45, 'z', ARM_O_R), 'arm_l': (-45, 'z', ARM_O_L)},
        'dance_a': {'arm_r': (45, 'z', ARM_O_R), 'arm_l': (-22.5, 'z', ARM_O_L),
                    'leg_r': (22.5, 'z', LEG_O), 'shoe_r': (22.5, 'z', LEG_O)},
        'dance_b': {'arm_r': (22.5, 'z', ARM_O_R), 'arm_l': (-45, 'z', ARM_O_L),
                    'leg_l': (-22.5, 'z', LEG_O), 'shoe_l': (-22.5, 'z', LEG_O)},
        'laugh': {'arm_r': (22.5, 'x', ARM_O_R), 'arm_l': (22.5, 'x', ARM_O_L)},
        'offer': {'arm_r': (45, 'x', ARM_O_R)},
        'float': {'leg_r': (22.5, 'x', LEG_O), 'shoe_r': (22.5, 'x', LEG_O),
                  'arm_r': (22.5, 'z', ARM_O_R), 'arm_l': (-22.5, 'z', ARM_O_L)},
    }[name]
    if extra:
        rots = dict(rots, **extra)
    els = []
    for k, p in P.items():
        r = rots.get(k)
        # partes que acompañan a otra (p.ej. 'skirt' no rota)
        els.append(p.element(rot=r))
    return els


def head_parts(at, c, style='short'):
    """Cabeza: devuelve (partes fijas, rect_cara) - la cara se dibuja por expresión."""
    P = {}
    skin = c['skin']
    P['head'] = Part(at, 'head', [5, 8, 5], [11, 14.4, 11], skin, faces=['south', 'east', 'west', 'up', 'down'])
    hair = c['hair']
    hs = lambda a, f, r: hair_strands(a, f, r)
    if style == 'short':
        P['hair_top'] = Part(at, 'hair_top', [4.7, 13.6, 4.7], [11.3, 15.0, 11.3], hair, paint=hs)
        P['hair_back'] = Part(at, 'hair_back', [4.7, 10.2, 10.6], [11.3, 14.0, 11.3], hair, paint=hs)
        P['hair_l'] = Part(at, 'hair_l', [4.6, 11.4, 4.8], [5.0, 14.0, 11.2], hair, paint=hs)
        P['hair_r'] = Part(at, 'hair_r', [11.0, 11.4, 4.8], [11.4, 14.0, 11.2], hair, paint=hs)
        P['fringe'] = Part(at, 'fringe', [5, 13.4, 4.6], [11, 14.2, 5], hair, paint=hs)
    elif style == 'emo':
        P['hair_top'] = Part(at, 'hair_top', [4.6, 13.6, 4.6], [11.4, 15.2, 11.4], hair, paint=hs)
        P['hair_back'] = Part(at, 'hair_back', [4.6, 9.4, 10.6], [11.4, 14.0, 11.4], hair, paint=hs)
        P['hair_l'] = Part(at, 'hair_l', [4.5, 10.0, 4.8], [5.0, 14.0, 11.2], hair, paint=hs)
        P['hair_r'] = Part(at, 'hair_r', [11.0, 10.4, 4.8], [11.5, 14.0, 11.2], hair, paint=hs)
        P['fringe'] = Part(at, 'fringe', [6.6, 10.6, 4.5], [11.2, 14.2, 4.9], hair, paint=hs)
    elif style == 'bob':
        # bob ondulado a la altura del mentón + flequillo (Juli)
        P['hair_top'] = Part(at, 'hair_top', [4.5, 13.5, 4.5], [11.5, 15.1, 11.5], hair, paint=hs)
        P['hair_back'] = Part(at, 'hair_back', [4.3, 7.4, 10.4], [11.7, 14.6, 11.9], hair, paint=hs)
        P['hair_l'] = Part(at, 'hair_l', [3.8, 7.6, 4.9], [5.0, 14.4, 11.6], hair, paint=hs)
        P['hair_r'] = Part(at, 'hair_r', [11.0, 7.6, 4.9], [12.2, 14.4, 11.6], hair, paint=hs)
        P['wave_l'] = Part(at, 'wave_l', [3.4, 7.2, 6.0], [4.2, 9.6, 11.0], hair, paint=hs)
        P['wave_r'] = Part(at, 'wave_r', [11.8, 7.2, 6.0], [12.6, 9.6, 11.0], hair, paint=hs)
        P['fringe'] = Part(at, 'fringe', [4.9, 12.4, 4.5], [11.1, 14.3, 4.95], hair, paint=hs)
    elif style == 'bald':
        pass
    return P


def face_rect(at, w=6, h=6.4):
    r = at.alloc(w * 4, h * 4)
    return r


def face_element(at, r, skin, style, name, frm=(5, 8, 4.97), to=(11, 14.4, 4.97)):
    at.fill(r, hexc(skin), noise=0.04)
    draw_face(at, r, dict(style, skin=skin))
    return {'from': list(frm), 'to': list(to), 'faces': {'north': {'uv': at.uv(r), 'texture': '#0'}}, 'name': name}


def all_elements(P):
    return [p.element() for p in P.values()]


