"""Pieles (texturas) de los monstruos Java del mod (Diana 3D y el gigante), cuándo aparecen solos y sus comandos.
La textura calza con MonstruoModelo.java (128x128, una caja por pieza)."""
from PIL import Image, ImageDraw
import random
from canon.shim import *  # noqa: F401,F403
from canon import shim

CAJAS = {  # nombre: (u, v, ancho, alto, fondo)
    'pierna_d': (0, 0, 3, 20, 3), 'pierna_i': (12, 0, 3, 20, 3), 'torso': (24, 0, 8, 14, 4), 'brazo_d': (48, 0, 2, 28, 2),
    'brazo_i': (56, 0, 2, 28, 2), 'cuello': (64, 0, 2, 7, 2), 'cabeza': (72, 0, 8, 8, 8), 'falda': (0, 40, 10, 9, 6),
    'pelo_frente': (0, 60, 9, 14, 1), 'pelo_atras': (24, 60, 9, 16, 1)}


def caja(d, u, v, w, h, f, col, rnd, ruido=18):
    for x in range(u, u + 2 * (w + f)):
        for y in range(v, v + h + f):
            n = rnd.randint(-ruido, ruido)
            d.point((x, y), fill=tuple(max(0, min(255, c + n)) for c in col) + (255,))


def piel(path, paleta, cara=True, seed=7):
    rnd = random.Random(seed)
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, (u, v, w, h, f) in CAJAS.items():
        col = paleta['pelo'] if k.startswith('pelo') else paleta['ropa'] if k in ('torso', 'falda') else paleta['piel']
        caja(d, u, v, w, h, f, col, rnd)
    # venas en brazos y piernas
    for (u, v, w, h, f) in (CAJAS['brazo_d'], CAJAS['brazo_i'], CAJAS['pierna_d'], CAJAS['pierna_i']):
        for _ in range(6):
            x, y = rnd.randint(u, u + 2 * (w + f) - 1), rnd.randint(v + f, v + f + h - 4)
            for s in range(rnd.randint(2, 5)):
                d.point((x, y + s), fill=paleta['vena'] + (255,))
        d.rectangle([u, v + f + h - 3, u + 2 * (w + f) - 1, v + f + h - 1], fill=paleta['punta'] + (255,))  # dedos/pies oscuros
    # falda rota: huecos en el borde
    u, v, w, h, f = CAJAS['falda']
    for x in range(u, u + 2 * (w + f)):
        if rnd.random() < 0.45:
            d.line([x, v + f + h - rnd.randint(1, 4), x, v + f + h - 1], fill=(0, 0, 0, 0))
    # pelo: mechones y hueco donde se asoma la cara
    for k in ('pelo_frente', 'pelo_atras'):
        u, v, w, h, f = CAJAS[k]
        for x in range(u, u + 2 * (w + f)):
            if rnd.random() < 0.5:
                d.line([x, v + f, x, v + f + h - 1], fill=tuple(max(0, c - 18) for c in paleta['pelo']) + (255,))
            corte = rnd.randint(0, 3)
            if corte:
                d.line([x, v + f + h - corte, x, v + f + h - 1], fill=(0, 0, 0, 0))
    u, v, w, h, f = CAJAS['pelo_frente']
    d.rectangle([u + f + 3, v + f, u + f + 5, v + f + 7], fill=(0, 0, 0, 0))  # rendija: se le ve un ojo y la sonrisa
    # cara (frente de la cabeza: 8x8)
    u, v, w, h, f = CAJAS['cabeza']
    fx, fy = u + f, v + f
    if cara:
        d.rectangle([fx + 1, fy + 2, fx + 2, fy + 3], fill=(5, 5, 5, 255))
        d.rectangle([fx + 5, fy + 2, fx + 6, fy + 3], fill=(5, 5, 5, 255))
        d.point([(fx + 2, fy + 3), (fx + 5, fy + 3)], fill=(220, 220, 200, 255))  # pupilas diminutas
        d.line([fx + 1, fy + 4, fx + 1, fy + 5], fill=(60, 10, 10, 255))  # lágrimas negras
        d.line([fx, fy + 6, fx + 7, fy + 6], fill=(30, 0, 0, 255))  # sonrisa de oreja a oreja
        d.line([fx + 1, fy + 7, fx + 6, fy + 7], fill=(30, 0, 0, 255))
        for x in range(fx + 1, fx + 7, 2):
            d.point((x, fy + 6), fill=(225, 220, 190, 255))  # dientes
    else:
        d.rectangle([fx + 1, fy + 1, fx + 6, fy + 6], fill=tuple(max(0, c - 25) for c in paleta['piel']) + (255,))
    im.save(path)


def build(c):
    shim.use(c)
    piel(c.path('assets/canonevent/textures/entity/diana.png'),
         {'piel': (176, 182, 170), 'vena': (70, 80, 95), 'punta': (40, 30, 30), 'ropa': (42, 36, 48), 'pelo': (14, 12, 14)}, True, 7)
    piel(c.path('assets/canonevent/textures/entity/gigante.png'),
         {'piel': (70, 66, 64), 'vena': (30, 25, 25), 'punta': (20, 15, 15), 'ropa': (30, 28, 30), 'pelo': (22, 20, 20)}, False, 11)
    c.text('entity.canonevent.diana', 'Diana')
    c.text('entity.canonevent.gigante', 'El Gigante')
    # aparecen solos: Diana de noche (más con miedo), el gigante de noche a lo lejos
    c.on('second', '''
execute if score #diana dv.cfg matches 1 if predicate canon:de_noche unless entity @e[type=canonevent:diana] as @a[gamemode=!spectator,gamemode=!creative,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:azar/1en900 run function canon:mj/diana_aparece
execute if score #diana dv.cfg matches 1 if predicate canon:de_noche unless entity @e[type=canonevent:diana] as @a[gamemode=!spectator,gamemode=!creative,scores={dv.miedo=60..},limit=1,sort=random] at @s if predicate canon:azar/1en300 run function canon:mj/diana_aparece
execute if score #sustos dv.cfg matches 1 if predicate canon:de_noche unless entity @e[type=canonevent:gigante] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if entity @s[y=50,dy=300] if predicate canon:azar/1en2400 run function canon:mj/gigante_aparece
''')
    F('mj/diana_aparece', 'scoreboard players set #ok dv.tmp 0\nexecute rotated ~ 0 positioned ^ ^ ^-18 run function canon:util/spot_search\n'
      'execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run summon canonevent:diana ~ ~ ~\nkill @e[type=marker,tag=dv_spot]\n'
      'execute if score #ok dv.tmp matches 1 run playsound canon:gen.respira_lenta hostile @s ^ ^ ^-6 0.6 0.8')
    F('mj/gigante_aparece', 'scoreboard players set #ok dv.tmp 0\nexecute rotated ~ 0 positioned ^-20 ^ ^60 run function canon:util/spot_search\n'
      'execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run summon canonevent:gigante ~ ~ ~\nkill @e[type=marker,tag=dv_spot]\n'
      'execute if score #ok dv.tmp matches 1 run tellraw @s {"text":"A lo lejos, entre la niebla, camina algo enorme.","color":"gray","italic":true}')
    F('admin/mj/diana', 'execute positioned ^ ^ ^8 run summon canonevent:diana ~ ~ ~')
    F('admin/mj/gigante', 'function canon:mj/gigante_aparece')
    c.admin('/function canon:admin/mj/diana', 'Diana 3D (se acerca cuando no la miras)')
    c.admin('/function canon:admin/mj/gigante', 'El Gigante a lo lejos')
