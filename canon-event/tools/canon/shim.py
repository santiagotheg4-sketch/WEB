"""Atajos para escribir módulos con funciones sueltas (F, A, pick...) en vez de c.F.
En build(c) de cada módulo: shim.use(c)."""
from canon.ctx import (txt, jt, btn, bubble, chat, say, menu, rig_summon, set_cmd, head, item_nbt, loot_item,
                       BuildError)  # noqa: F401

C = None
CMD = {}   # nombre de modelo -> CustomModelData (todos los módulos)


def use(c):
    global C
    C = c


def F(*a, **k):
    return C.F(*a, **k)


def A(*a, **k):
    return C.A(*a, **k)


def pick(*a, **k):
    return C.pick(*a, **k)


def models(names, start):
    """Registra modelos con CMD consecutivos desde `start`. Devuelve el dict."""
    for i, n in enumerate(names):
        CMD[n] = C.model(n, start + i)
    return CMD
