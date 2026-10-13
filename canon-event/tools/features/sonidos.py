"""Sonidos generados (pasos, puertas, golpes, respiraciones, susurros, latidos, viento, ambiente, persecución, voces).
Se generan una vez en tools/cache_sonidos/ y se copian al mod. Eventos: canon:gen.<nombre>.
"""
import os
import shutil
from canon.shim import *  # noqa: F401,F403
from canon import shim

CACHE = os.path.join(os.path.dirname(__file__), '..', 'cache_sonidos')
VOCES = {  # nombre: (texto, grave, voz)
    'diana_te_vi': ('Te vi dormir.', True, 'es+f4'),
    'diana_juan': ('¿Dónde está Juan?', True, 'es+f4'),
    'diana_detras': ('Estoy detrás de ti.', True, 'es+f4'),
    'diana_abre': ('Ábreme la puerta.', True, 'es+f4'),
    'diana_risa': ('Je je je je je.', True, 'es+f4'),
    'kevin_hey': ('¡Ey! ¿Me estás evitando?', False, 'es+m3'),
    'kevin_enojado': ('No me vuelvas a decir que no.', True, 'es+m3'),
    'kevin_te_veo': ('Te estoy viendo.', True, 'es+m3'),
    'abuela_mijo': ('Mijito, ábrale a la abuela.', True, 'es+f2'),
    'juli_santi': ('Santi, no te duermas todavía.', False, 'es+f3'),
    'nicolas_aqui': ('Aquí abajo hace frío.', True, 'es+m2'),
    'nombre_susurro': ('Oye. Oye. Voltea.', True, 'es+f4'),
    'contigo': ('No estás solo.', True, 'es+m4'),
}


def generar():
    from canon import audio as A
    os.makedirs(CACHE, exist_ok=True)
    lista = {}
    for v in range(4):
        lista[f'paso_madera{v}'] = lambda v=v: A.paso_madera(v)
    for v in range(3):
        lista[f'paso_tierra{v}'] = lambda v=v: A.paso_tierra(v)
        lista[f'puerta{v}'] = lambda v=v: A.cruje_puerta(v)
        lista[f'susurro{v}'] = lambda v=v: A.susurro(6 + v * 2, v)
    lista.update({
        'golpes3': lambda: A.golpes(3), 'golpes5': lambda: A.golpes(5, 1.2), 'golpe1': lambda: A.golpes(1, 0.8),
        'respira_lenta': lambda: A.respiracion(True), 'respira_rapida': lambda: A.respiracion(False),
        'latido': lambda: A.latido(False), 'latido_rapido': lambda: A.latido(True),
        'viento': lambda: A.viento(), 'drone': lambda: A.drone(), 'drone_grave': lambda: A.drone(base=41.2),
        'persecucion': lambda: A.persecucion(), 'stinger': lambda: A.stinger(), 'estatica': lambda: A.lluvia_estatica(),
        'guitarra': lambda: A.guitarra_triste(), 'silbido_cerca': lambda: A.silbido(True), 'silbido_lejos': lambda: A.silbido(False),
    })
    for k, (txt, grave, voz) in VOCES.items():
        lista['voz_' + k] = lambda txt=txt, grave=grave, voz=voz: A.voz(txt, grave, True, voz)
    hechos = 0
    for nombre, fn in lista.items():
        p = os.path.join(CACHE, nombre + '.ogg')
        if not os.path.exists(p):
            A.save(p, fn())
            hechos += 1
    return list(lista), hechos


def build(c):
    shim.use(c)
    nombres, hechos = generar()
    dst = c.path('assets/canon/sounds/gen')
    os.makedirs(dst, exist_ok=True)
    for n in nombres:
        shutil.copy(os.path.join(CACHE, n + '.ogg'), os.path.join(dst, n + '.ogg'))
    grupos = {'paso_madera': 4, 'paso_tierra': 3, 'puerta': 3, 'susurro': 3}
    for g, k in grupos.items():
        c.sound('gen.' + g, [{'name': f'canon:gen/{g}{i}'} for i in range(k)], subtitle='subtitulos.canon.' + g)
    stream = {'viento', 'drone', 'drone_grave', 'persecucion', 'guitarra'}
    for n in nombres:
        if any(n.startswith(g) and n[len(g):].isdigit() for g in grupos):
            continue
        c.sound('gen.' + n, [{'name': f'canon:gen/{n}', 'stream': n in stream}], subtitle='subtitulos.canon.' + n)
    subs = {'paso_madera': 'Pasos en la madera', 'paso_tierra': 'Pasos afuera', 'puerta': 'Una puerta cruje', 'susurro': 'Alguien susurra',
            'golpes3': 'Tocan la puerta', 'golpes5': 'Golpean la puerta', 'golpe1': 'Un golpe', 'respira_lenta': 'Alguien respira',
            'respira_rapida': 'Respiración agitada', 'latido': 'Tu corazón', 'latido_rapido': 'Tu corazón se acelera', 'viento': 'Viento',
            'drone': 'Algo zumba', 'drone_grave': 'Algo zumba', 'persecucion': 'Te persiguen', 'stinger': '¡!', 'estatica': 'Estática',
            'guitarra': 'Alguien toca guitarra', 'silbido_cerca': 'Un silbido lejano', 'silbido_lejos': 'Un silbido cercano'}
    for k in VOCES:
        subs['voz_' + k] = 'Una voz'
    for k, v in subs.items():
        c.text('subtitulos.canon.' + k, v)
    print(f'  sonidos generados nuevos: {hechos} de {len(nombres)}')
