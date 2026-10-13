"""Criaturas del agua (Java: Marina.java, Mar.java): La Ahogada, que se asoma del agua o se para en la orilla y te llama,
y el Leviatán, una serpiente enorme que da vueltas debajo de tu bote. Aquí: sus pieles, sus voces y sonidos, y comandos.
Las texturas calzan con MarModelos.java (128x128)."""
import os
import random
import shutil
from PIL import Image, ImageDraw
from canon.shim import *  # noqa: F401,F403
from canon import shim

CACHE = os.path.join(os.path.dirname(__file__), '..', 'cache_sonidos')
AH = {'cabeza': (0, 0, 8, 9, 8), 'pelo_frente': (32, 0, 9, 18, 1), 'pelo_atras': (56, 0, 9, 22, 1), 'pelo_lado': (80, 0, 1, 16, 8),
      'torso': (0, 24, 8, 12, 4), 'vestido': (24, 24, 10, 14, 6), 'brazo_d': (0, 44, 2, 24, 2), 'brazo_i': (8, 44, 2, 24, 2),
      'dedos': (16, 44, 1, 6, 1), 'pierna_d': (24, 48, 3, 18, 3), 'pierna_i': (36, 48, 3, 18, 3)}
LV = {'cabeza': (0, 0, 12, 10, 18), 'mandibula': (60, 0, 10, 4, 16), 'seg0': (0, 28, 10, 10, 16), 'seg1': (52, 28, 10, 10, 16),
      'seg2': (0, 54, 10, 10, 16), 'seg3': (52, 54, 10, 10, 16), 'seg4': (0, 80, 8, 8, 16), 'cola': (48, 80, 1, 12, 14),
      'espina': (104, 28, 2, 5, 3), 'diente': (112, 0, 1, 3, 1)}
VOCES = {'ven': 'Ven... ven al agua.', 'tibia': 'El agua está tibia. Métete.', 'ayuda': '¡Ayúdame! ¡Me estoy ahogando!',
         'abajo': 'Aquí abajo no duele.', 'nombre': 'Te estaba esperando. Ven conmigo.'}


def _caja(d, rnd, box, col, ruido=14):
    u, v, w, h, f = box
    for x in range(u, u + 2 * (w + f)):
        for y in range(v, v + h + f):
            n = rnd.randint(-ruido, ruido)
            d.point((x, y), fill=tuple(max(0, min(255, c + n)) for c in col) + (255,))


def _frente(box):
    u, v, w, h, f = box
    return u + f, v + f, w, h


def piel_ahogada(path):
    rnd = random.Random(23)
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    PIEL, PELO, VEST = (168, 184, 188), (14, 20, 18), (196, 198, 186)
    for k, box in AH.items():
        col = PELO if k.startswith('pelo') else VEST if k in ('torso', 'vestido') else PIEL
        _caja(d, rnd, box, col)
    # venas azules y manchas moradas en la piel
    for k in ('cabeza', 'brazo_d', 'brazo_i', 'pierna_d', 'pierna_i', 'dedos'):
        u, v, w, h, f = AH[k]
        W, H = 2 * (w + f), h + f
        for _ in range(max(2, W * H // 16)):
            x, y = u + rnd.randrange(W), v + rnd.randrange(H)
            d.point((x, y), fill=(70, 90, 120, 255) if rnd.random() < 0.7 else (110, 80, 110, 255))
    for k in ('dedos', 'brazo_d', 'brazo_i'):  # uñas/puntas negras
        u, v, w, h, f = AH[k]
        d.rectangle([u, v + f + h - 2, u + 2 * (w + f) - 1, v + f + h - 1], fill=(30, 30, 35, 255))
    # vestido sucio: algas y barro, borde roto
    for k in ('torso', 'vestido'):
        u, v, w, h, f = AH[k]
        W, H = 2 * (w + f), h + f
        for _ in range(W * H // 6):
            x, y = u + rnd.randrange(W), v + rnd.randrange(H)
            d.point((x, y), fill=(90, 110, 70, 255) if rnd.random() < 0.6 else (110, 90, 70, 255))
    u, v, w, h, f = AH['vestido']
    for x in range(u, u + 2 * (w + f)):
        if rnd.random() < 0.55:
            d.line([x, v + f + h - rnd.randint(1, 5), x, v + f + h - 1], fill=(0, 0, 0, 0))
    # pelo mojado: mechones brillantes y puntas que gotean, con huecos
    for k in ('pelo_frente', 'pelo_atras', 'pelo_lado'):
        u, v, w, h, f = AH[k]
        for x in range(u, u + 2 * (w + f)):
            if rnd.random() < 0.35:
                d.line([x, v + f, x, v + f + h - 1], fill=(36, 48, 44, 255))
            corte = rnd.randint(0, 4)
            if corte:
                d.line([x, v + f + h - corte, x, v + f + h - 1], fill=(0, 0, 0, 0))
    fx, fy, fw, fh = _frente(AH['pelo_frente'])
    for y in range(fy + 2, fy + 11):  # rendija: se le ve un ojo y la boca
        for x in (fx + 4, fx + 5):
            d.point((x, y), fill=(0, 0, 0, 0))
    d.point((fx + 3, fy + 8), fill=(0, 0, 0, 0))
    # cara
    fx, fy, fw, fh = _frente(AH['cabeza'])
    d.rectangle([fx + 1, fy + 3, fx + 2, fy + 4], fill=(10, 10, 14, 255))
    d.rectangle([fx + 5, fy + 3, fx + 6, fy + 4], fill=(10, 10, 14, 255))
    d.point([(fx + 2, fy + 4), (fx + 5, fy + 4)], fill=(230, 235, 240, 255))
    d.rectangle([fx + 3, fy + 6, fx + 4, fy + 8], fill=(20, 8, 12, 255))  # boca abierta
    d.point([(fx + 2, fy + 6), (fx + 5, fy + 6)], fill=(80, 90, 120, 255))  # labios morados
    d.line([fx + 1, fy + 5, fx + 1, fy + 7], fill=(60, 70, 80, 255))  # agua que le chorrea
    im.save(path)


def ojos_ahogada(path):
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fx, fy, fw, fh = _frente(AH['cabeza'])
    d.point([(fx + 2, fy + 4), (fx + 5, fy + 4)], fill=(220, 240, 255, 255))
    im.save(path)


def piel_leviatan(path):
    rnd = random.Random(77)
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, box in LV.items():
        col = (225, 215, 180) if k in ('diente',) else (60, 58, 52) if k == 'espina' else (34, 46, 52)
        _caja(d, rnd, box, col, 10)
        u, v, w, h, f = box
        if k not in ('diente', 'espina'):
            d.rectangle([u + f + w, v, u + f + 2 * w - 1, v + f - 1], fill=(120, 128, 118, 255))  # panza pálida
            W, H = 2 * (w + f), h + f
            for _ in range(W * H // 10):  # escamas
                x, y = u + rnd.randrange(W), v + rnd.randrange(H)
                d.point((x, y), fill=(22, 30, 36, 255))
            for _ in range(W * H // 70):  # percebes y cicatrices
                x, y = u + rnd.randrange(W - 1), v + rnd.randrange(H - 1)
                d.rectangle([x, y, x + 1, y], fill=(170, 165, 150, 255) if rnd.random() < 0.6 else (90, 40, 40, 255))
    # boca por dentro
    u, v, w, h, f = LV['mandibula']
    d.rectangle([u + f, v, u + f + w - 1, v + f - 1], fill=(70, 10, 16, 255))
    u, v, w, h, f = LV['cabeza']
    d.rectangle([u + f + w, v, u + f + 2 * w - 1, v + f - 1], fill=(60, 8, 12, 255))
    # ojos a los lados de la cabeza, cerca de la punta
    oeste = (u + f - 4, v + f + 2)
    este = (u + f + w + 2, v + f + 2)
    for ox, oy in (oeste, este):
        d.rectangle([ox, oy, ox + 2, oy + 2], fill=(200, 170, 40, 255))
        d.line([ox + 1, oy, ox + 1, oy + 2], fill=(0, 0, 0, 255))
    im.save(path)


def ojos_leviatan(path):
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    u, v, w, h, f = LV['cabeza']
    for ox, oy in ((u + f - 4, v + f + 2), (u + f + w + 2, v + f + 2)):
        d.rectangle([ox, oy, ox + 2, oy + 2], fill=(255, 220, 60, 255))
        d.line([ox + 1, oy, ox + 1, oy + 2], fill=(20, 0, 0, 255))
    im.save(path)


def sonidos():
    from canon import audio as A
    lista = {'mar_canto': A.canto, 'mar_chapoteo': A.chapoteo, 'mar_grito': A.grito, 'mar_gemido': A.gemido}
    for k, t in VOCES.items():
        lista['mar_voz_' + k] = lambda t=t: A.voz_agua(t)
    for n, fn in lista.items():
        p = os.path.join(CACHE, n + '.ogg')
        if not os.path.exists(p):
            A.save(p, fn())
    return list(lista)


def build(c):
    shim.use(c)
    c.config('mar', 'Criaturas del agua (la Ahogada, el Leviatán)', 1)
    piel_ahogada(c.path('assets/canonevent/textures/entity/ahogada.png'))
    ojos_ahogada(c.path('assets/canonevent/textures/entity/ahogada_ojos.png'))
    piel_leviatan(c.path('assets/canonevent/textures/entity/leviatan.png'))
    ojos_leviatan(c.path('assets/canonevent/textures/entity/leviatan_ojos.png'))
    c.text('entity.canonevent.ahogada', 'La Ahogada')
    c.text('entity.canonevent.leviatan', 'El Leviatán')
    dst = c.path('assets/canon/sounds/mar')
    os.makedirs(dst, exist_ok=True)
    subs = {'mar_canto': 'Alguien canta debajo del agua', 'mar_chapoteo': 'Algo chapotea', 'mar_grito': 'Un grito ahogado',
            'mar_gemido': 'Algo enorme gime en el fondo'}
    for n in sonidos():
        shutil.copy(os.path.join(CACHE, n + '.ogg'), os.path.join(dst, n + '.ogg'))
        ev = n.replace('mar_', 'mar.', 1)
        c.sound(ev, [{'name': f'canon:mar/{n}', 'attenuation_distance': 48 if n != 'mar_gemido' else 96}],
                subtitle='subtitulos.canon.' + n)
        c.text('subtitulos.canon.' + n, subs.get(n, 'Una voz te llama desde el agua'))
    F('admin/mar/ahogada', 'execute positioned ^ ^ ^12 run summon canonevent:ahogada ~ ~ ~')
    F('admin/mar/orilla', 'execute positioned ^ ^ ^10 run summon canonevent:ahogada ~ ~ ~ {Tags:["dv_orilla"]}')
    F('admin/mar/leviatan', 'execute positioned ^ ^-8 ^20 run summon canonevent:leviatan ~ ~ ~')
    c.admin('/function canon:admin/mar/ahogada', 'La Ahogada (ponla en agua honda: se asoma y te llama)')
    c.admin('/function canon:admin/mar/orilla', 'La Ahogada parada en la orilla, mirándote')
    c.admin('/function canon:admin/mar/leviatan', 'El Leviatán debajo de ti (estando en el mar)')
