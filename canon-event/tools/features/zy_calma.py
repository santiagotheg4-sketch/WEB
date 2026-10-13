"""Ritmo del miedo: después de un susto grande hay un rato de calma (nada nuevo aparece), para que la tensión
suba poco a poco y los sustos lleguen cuando uno ya bajó la guardia. Se aplica a todas las apariciones al azar."""
import re
from canon.shim import *  # noqa: F401,F403
from canon import shim

CALMA = 150  # segundos de calma después de un susto


def build(c):
    shim.use(c)
    c.objective('dv.calma')
    c.patch('x/jumpscare', lambda s: s if 'dv.calma' in s else s.rstrip('\n') + f'\nscoreboard players set @s dv.calma {CALMA}\n')
    c.on('second', 'scoreboard players remove @a[scores={dv.calma=1..}] dv.calma 1')

    def calma(s):
        out = []
        for l in s.split('\n'):
            if 'predicate canon:azar/' in l and 'dv.calma' not in l:
                l = re.sub(r'(as @a\[[^\]]*\] at @s)', r'\1 unless score @s dv.calma matches 1..', l, count=1)
            out.append(l)
        return '\n'.join(out)
    c.patch('extra/second', calma)
