"""Personajes que ya no existen en el mod (Valery y Santiago, el ex de Mari): si quedaron en un mundo viejo, se borran solos."""
from canon.shim import *  # noqa: F401,F403
from canon import shim

QUITADOS = ('dv_valery', 'dv_exsanti')


def build(c):
    shim.use(c)
    F('limpieza/quitar', '\n'.join(f'execute as @e[type=zombie,tag={t}] at @s run function canon:rig/despawn' for t in QUITADOS) +
      '\nscoreboard objectives remove dv.val\nscoreboard objectives remove dv.valp\nscoreboard objectives remove dv.ex\nscoreboard objectives remove dv.soymari')
    c.on('load', 'function canon:limpieza/quitar')
    c.on('second', '\n'.join(f'execute as @e[type=zombie,tag={t}] at @s run function canon:rig/despawn' for t in QUITADOS))
