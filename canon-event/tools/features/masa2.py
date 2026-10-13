"""Catacumbas mejoradas: La Masa ahora es un monstruo Java de verdad (canonevent:masa), grande y animado,
que te busca por los pasillos sin atravesar paredes. Kevin corre detrás de ti siguiendo tu rastro (Rastro.java)
y grita cosas mientras huyen. La textura calza con MasaModelo.java (128x128)."""
import random
from PIL import Image, ImageDraw
from canon.shim import *  # noqa: F401,F403
from canon import shim

CAJAS = {  # nombre: (u, v, ancho, alto, fondo)
    'torso': (0, 0, 22, 22, 22), 'joroba': (0, 44, 16, 8, 14), 'cabeza': (60, 44, 12, 10, 12), 'mandibula': (0, 66, 10, 4, 10),
    'brazo_d': (40, 66, 4, 18, 4), 'brazo_i': (56, 66, 4, 18, 4), 'ante': (72, 66, 3, 22, 3), 'garra': (96, 66, 1, 7, 1),
    'diente': (108, 66, 1, 3, 1), 'pierna_d': (0, 88, 6, 14, 6), 'pierna_i': (24, 88, 6, 14, 6), 'canilla_d': (48, 88, 4, 14, 4),
    'canilla_i': (64, 88, 4, 14, 4), 'espalda_d': (80, 92, 2, 16, 2), 'espalda_i': (88, 92, 2, 16, 2), 'espina': (96, 92, 2, 5, 2)}
CARNE = (142, 59, 63)


def _caja(d, rnd, u, v, w, h, f, col, ruido=22):
    for x in range(u, u + 2 * (w + f)):
        for y in range(v, v + h + f):
            n = rnd.randint(-ruido, ruido)
            d.point((x, y), fill=tuple(max(0, min(255, c + n)) for c in col) + (255,))


def _frente(u, v, w, h, f):
    """Rectángulo de la cara de adelante (norte) de una caja."""
    return u + f, v + f, w, h


def piel(path):
    rnd = random.Random(61)
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, (u, v, w, h, f) in CAJAS.items():
        col = (225, 215, 190) if k in ('garra', 'diente', 'espina') else (40, 8, 10) if k == 'mandibula' else \
            (120, 48, 52) if k in ('ante', 'canilla_d', 'canilla_i', 'espalda_d', 'espalda_i') else CARNE
        _caja(d, rnd, u, v, w, h, f, col)
    # venas, costillas y llagas en la carne
    for k in ('torso', 'joroba', 'cabeza', 'brazo_d', 'brazo_i', 'pierna_d', 'pierna_i'):
        u, v, w, h, f = CAJAS[k]
        W, H = 2 * (w + f), h + f
        for _ in range(W * H // 14):
            x, y = u + rnd.randrange(W), v + rnd.randrange(H)
            for s in range(rnd.randint(2, 6)):
                d.point((x + rnd.randint(-1, 1), y + s), fill=(70, 18, 24, 255))
        for _ in range(W * H // 60):
            x, y = u + rnd.randrange(W - 2), v + rnd.randrange(H - 2)
            d.rectangle([x, y, x + 1, y + 1], fill=(205, 170, 120, 255))  # pus
    # costillas en los lados del torso
    u, v, w, h, f = CAJAS['torso']
    for lado in (u, u + f + w):
        for i in range(5):
            y = v + f + 3 + i * 4
            d.line([lado + 2, y, lado + f - 3, y + 1], fill=(222, 210, 185, 255))
    # pecho: bocas y ojos metidos en la carne
    fx, fy, fw, fh = _frente(*CAJAS['torso'])
    d.rectangle([fx + 6, fy + 11, fx + 15, fy + 14], fill=(25, 0, 0, 255))
    for x in range(fx + 6, fx + 16, 2):
        d.point((x, fy + 11), fill=(230, 225, 200, 255))
        d.point((x + 1, fy + 14), fill=(230, 225, 200, 255))
    for ox, oy in ((4, 4), (16, 3), (10, 7), (18, 17)):
        d.rectangle([fx + ox, fy + oy, fx + ox + 1, fy + oy + 1], fill=(235, 230, 205, 255))
        d.point((fx + ox, fy + oy), fill=(10, 0, 0, 255))
    # cara: muchos ojos chiquitos y una boca rajada
    fx, fy, fw, fh = _frente(*CAJAS['cabeza'])
    d.rectangle([fx, fy, fx + fw - 1, fy + fh - 1], fill=(110, 40, 44, 255))
    for ox, oy in ((2, 2), (8, 1), (5, 3), (9, 4), (1, 5)):
        d.rectangle([fx + ox, fy + oy, fx + ox + 1, fy + oy + 1], fill=(245, 240, 220, 255))
        d.point((fx + ox + 1, fy + oy + 1), fill=(0, 0, 0, 255))
    d.rectangle([fx + 1, fy + 7, fx + fw - 2, fy + 9], fill=(20, 0, 0, 255))
    # dentro de la boca (arriba de la mandíbula y abajo de la cabeza): oscuro con encías
    u, v, w, h, f = CAJAS['mandibula']
    d.rectangle([u + f, v, u + f + w - 1, v + f - 1], fill=(90, 10, 16, 255))
    u, v, w, h, f = CAJAS['cabeza']
    d.rectangle([u + f + w, v, u + f + 2 * w - 1, v + f - 1], fill=(60, 6, 10, 255))
    # garras y dientes amarillentos con punta oscura
    for k in ('garra', 'diente', 'espina'):
        u, v, w, h, f = CAJAS[k]
        d.line([u, v + f + h - 1, u + 2 * (w + f) - 1, v + f + h - 1], fill=(60, 50, 40, 255))
    im.save(path)


def ojos(path):
    """Lo que brilla en la oscuridad: los ojos de la cara y del pecho, y la boca por dentro."""
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fx, fy, fw, fh = _frente(*CAJAS['cabeza'])
    for ox, oy in ((2, 2), (8, 1), (5, 3), (9, 4), (1, 5)):
        d.rectangle([fx + ox, fy + oy, fx + ox + 1, fy + oy + 1], fill=(255, 235, 200, 255))
        d.point((fx + ox + 1, fy + oy + 1), fill=(255, 30, 20, 255))
    d.line([fx + 2, fy + 8, fx + fw - 3, fy + 8], fill=(160, 0, 0, 255))
    fx, fy, fw, fh = _frente(*CAJAS['torso'])
    for ox, oy in ((4, 4), (16, 3), (10, 7), (18, 17)):
        d.point((fx + ox + 1, fy + oy + 1), fill=(255, 40, 30, 255))
    im.save(path)


def build(c):
    shim.use(c)
    piel(c.path('assets/canonevent/textures/entity/masa.png'))
    ojos(c.path('assets/canonevent/textures/entity/masa_ojos.png'))
    c.text('entity.canonevent.masa', 'La Masa')

    # la Masa de las catacumbas ahora es la de Java
    c.patch('masa/spawn', lambda s: '''
kill @e[type=canonevent:masa]
summon canonevent:masa ~ ~ ~ {Rotation:[90f,0f]}
playsound canon:masa.rugido hostile @a[tag=dv_kpart] ~ ~ ~ 2 0.6
execute as @e[type=zombie,tag=dv_kevin] run function canon:k4/oyo
''')
    # la etiqueta va ANTES del tp: si Kevin cae en un chunk sin cargar se guarda en disco y la etiqueta se perdería
    c.patch('kevin/cata/enter', lambda s: s if 'dv_rastro' in s else s.replace(
        'execute as @e[type=zombie,tag=dv_kevin] in minecraft:overworld run tp', 'tag @e[type=zombie,tag=dv_kevin] add dv_rastro\nexecute as @e[type=zombie,tag=dv_kevin] in minecraft:overworld run tp', 1))
    c.on('second', 'execute if score #kev dv.dev matches 3 run tag @e[type=zombie,tag=dv_kevin,tag=!dv_rastro,x=19990,y=-60,z=19990,dx=72,dy=20,dz=72] add dv_rastro')
    c.patch('kevin/cata/cleanup', lambda s: s if 'canonevent:masa' in s else
            'kill @e[type=canonevent:masa]\ntag @e[type=zombie,tag=dv_kevin] remove dv_rastro\n' + s)
    # Kevin no camina a través de las paredes: en las catacumbas lo mueve el rastro (Java)
    c.patch('kevin/tick2', lambda s: s.replace('execute if score @s dv.mode matches 0 run function canon:kevin/m_follow',
                                               'execute if score @s dv.mode matches 0 unless entity @s[tag=dv_rastro] run function canon:kevin/m_follow'))
    c.patch('kevin/cata/tick2', lambda s: s if 'k4/' in s else s.rstrip('\n') + '\n' + '\n'.join([
        'execute if entity @e[type=canonevent:masa] if score #m40 dv.clock matches 0 if predicate canon:azar/1en5 as @e[type=zombie,tag=dv_kevin,limit=1] run function canon:k4/grita',
        'execute if entity @e[type=canonevent:masa] if score #m10 dv.clock matches 0 as @a[tag=dv_kpart] at @s if entity @e[type=canonevent:masa,distance=..10] run function canon:k4/cerca',
        'execute if score #kt dv.dev matches 200 run tellraw @a[tag=dv_kpart] {"text":"Kevin: Si oyen algo arrastrándose... no es nada. Seguro. Casi seguro.","color":"#ffb347","italic":true}',
        'execute if score #kt dv.dev matches 900 as @a[tag=dv_kpart] at @s run playsound canon:gen.voz_contigo hostile @s ^ ^ ^-6 0.7 0.6',
        'execute if score #kt dv.dev matches 1500 run tellraw @a[tag=dv_kpart] {"text":"Las velas se apagan solas, una por una, detrás de ustedes.","color":"gray","italic":true}',
    ]) + '\n')
    F('k4/oyo', 'tellraw @a[tag=dv_kpart] {"text":"Kevin: ...¿Oyeron eso? Díganme que fue la tripa de alguien.","color":"#ffb347","italic":true}')
    pick('k4/grita', [
        'tellraw @a[tag=dv_kpart] {"text":"Kevin: ¡CORRAN! ¡NO MIREN ATRÁS!","color":"#ffb347","bold":true}',
        'tellraw @a[tag=dv_kpart] {"text":"Kevin: ¡Por aquí! ¡No, no, por AQUÍ!","color":"#ffb347","bold":true}',
        'tellraw @a[tag=dv_kpart] {"text":"Kevin: ¡Jajaja...! No, no es chiste. ¡CORRAN!","color":"#ffb347","bold":true}',
        'tellraw @a[tag=dv_kpart] {"text":"Kevin: ¡LA LLAVE! ¡¿Alguien tiene la llave?!","color":"#ffb347","bold":true}',
        'tellraw @a[tag=dv_kpart] {"text":"Kevin: ¡Me pisó! ¡Esa cosa me pisó el pie!","color":"#ffb347","bold":true}',
        'tellraw @a[tag=dv_kpart] {"text":"Kevin: ¡Yo voy detrás! ¡Ustedes sigan!","color":"#ffb347","bold":true}',
    ])
    F('k4/cerca', '''
playsound canon:gen.latido hostile @s ~ ~ ~ 1 1.3
title @s actionbar {"text":"Está justo detrás de ti","color":"#c94a4a","italic":true}
''')
    F('admin/mj/masa', 'execute positioned ^ ^ ^10 run summon canonevent:masa ~ ~ ~')
    c.admin('/function canon:admin/mj/masa', 'La Masa (catacumbas): te persigue por los pasillos sin atravesar paredes')
