"""La canción de Santi («Noches de neón») en la discoteca de Kevin y en la rocola. La fiesta dura lo que dura la canción,
con extras durante la canción: Kevin la presenta, fuegos en el coro, un apagón en el que aparece alguien entre los que bailan."""
import os
import shutil
from canon.shim import *  # noqa: F401,F403
from canon import shim

MUSICA = os.path.join(os.path.dirname(__file__), '..', 'musica')
FIN = 3200  # ticks que dura la parte buena de la fiesta (la canción dura 158 s)


def mono():
    src = os.path.join(MUSICA, 'noches_de_neon.ogg')
    dst = os.path.join(MUSICA, 'noches_de_neon_mono.ogg')
    if not os.path.exists(dst):
        import soundfile as sf
        x, sr = sf.read(src, dtype='float32')
        x = x.mean(axis=1) if x.ndim > 1 else x
        with sf.SoundFile(dst, 'w', sr, 1, format='OGG', subtype='VORBIS') as f:
            for i in range(0, len(x), sr):
                f.write(x[i:i + sr])
    return dst


def build(c):
    shim.use(c)
    if not os.path.exists(os.path.join(MUSICA, 'noches_de_neon.ogg')):
        return
    d = c.path('assets/canon/sounds/musica')
    os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(MUSICA, 'noches_de_neon.ogg'), os.path.join(d, 'noches_de_neon.ogg'))
    shutil.copy(mono(), os.path.join(d, 'noches_de_neon_mono.ogg'))
    c.sound('kevin.techno', [{'name': 'canon:musica/noches_de_neon', 'stream': True}], subtitle='subtitulos.canon.neon', replace=True)
    c.sound('musica.noches_de_neon', [{'name': 'canon:musica/noches_de_neon_mono', 'stream': True, 'attenuation_distance': 40}],
            subtitle='subtitulos.canon.neon')
    c.text('subtitulos.canon.neon', '♪ Noches de neón — Santi')

    # la fiesta dura toda la canción; lo malo pasa después
    def fiesta(s):
        if 'k3/' in s:
            return s
        for a, b in (('matches ..899 ', f'matches ..{FIN - 1} '), ('matches 900 ', f'matches {FIN} '), ('matches 960 ', f'matches {FIN + 60} '),
                     ('matches 1040 ', f'matches {FIN + 140} '), ('matches 1080 ', f'matches {FIN + 180} ')):
            s = s.replace(a, b)
        return s.rstrip('\n') + '\n' + '\n'.join([
            'execute if score #kt dv.dev matches 40 run function canon:k3/presenta',
            'execute if score #kt dv.dev matches 1250 run function canon:k3/coro',
            'execute if score #kt dv.dev matches 2350 run function canon:k3/coro',
            'execute if score #kt dv.dev matches 1800 run function canon:k3/apagon',
            'execute if score #kt dv.dev matches 1860 run function canon:k3/vuelve_luz',
            f'execute if score #kt dv.dev matches {FIN - 80} run tellraw @a[tag=dv_kpart] {{"text":"Kevin: ¡OTRA! ¡OTRA! ...¿por qué se apagó todo?","color":"#ffd27a","italic":true}}',
        ]) + '\n'
    c.patch('kevin/fiesta/tick', fiesta)
    F('k3/presenta', '''
title @a[tag=dv_kpart] times 10 60 20
title @a[tag=dv_kpart] subtitle {"text":"Noches de neón — Santi","color":"#ff4fd8","italic":true}
title @a[tag=dv_kpart] title {"text":"♪ ♪ ♪","color":"#4fe3ff","bold":true}
tellraw @a[tag=dv_kpart] {"text":"Kevin: ¡ESTA ES DE SANTI! ¡NOCHES DE NEÓN! ¡TODO EL MUNDO A BAILAR!","color":"#ffb347","bold":true}
''')
    F('k3/coro', '''
execute at @e[type=marker,tag=dv_fiesta_c] run summon minecraft:firework_rocket ~3 ~1 ~3 {LifeTime:20,FireworksItem:{id:"minecraft:firework_rocket",Count:1b,tag:{Fireworks:{Explosions:[{Type:1,Colors:[I;16731096,5235711],FadeColors:[I;16777215]}]}}}}
execute at @e[type=marker,tag=dv_fiesta_c] run summon minecraft:firework_rocket ~-3 ~1 ~-3 {LifeTime:20,FireworksItem:{id:"minecraft:firework_rocket",Count:1b,tag:{Fireworks:{Explosions:[{Type:4,Colors:[I;5235711,16766720]}]}}}}
tellraw @a[tag=dv_kpart] {"text":"Kevin: ¡EL CORO! ¡TODOS!","color":"#ffb347","italic":true}
''')
    F('k3/apagon', '''
effect give @a[tag=dv_kpart] minecraft:blindness 3 0 true
playsound minecraft:block.lever.click master @a[tag=dv_kpart] ~ ~ ~ 1 0.5
tellraw @a[tag=dv_kpart] {"text":"Se fue la luz. La música sigue.","color":"gray","italic":true}
execute as @a[tag=dv_kpart,limit=1,sort=random] at @s run function canon:k3/alguien
''')
    F('k3/alguien', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nscoreboard players set #quien dv.tmp 1\nscoreboard players set #ok dv.tmp 0\n'
      'execute rotated ~ 0 positioned ^2 ^ ^5 run function canon:util/spot_search\n'
      'execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:acecho/aparecer\nkill @e[type=marker,tag=dv_spot]')
    F('k3/vuelve_luz', 'tellraw @a[tag=dv_kpart] {"text":"Volvió la luz. Entre los que bailan hay alguien que nadie invitó.","color":"#c94a4a","italic":true}')
    # la rocola a veces pone la canción de Santi
    c.patch('furn/rocola_play', lambda s: s if 'noches_de_neon' in s else s.replace(
        'playsound canon:music.rocola record @a[distance=..32] ~ ~ ~ 0.7 1',
        'scoreboard players set #rq dv.tmp 1\nexecute if predicate canon:azar/1en2 run scoreboard players set #rq dv.tmp 2\n'
        'execute if score #rq dv.tmp matches 1 run playsound canon:music.rocola record @a[distance=..32] ~ ~ ~ 0.7 1\n'
        'execute if score #rq dv.tmp matches 2 run playsound canon:musica.noches_de_neon record @a[distance=..40] ~ ~ ~ 1 1\n'
        'execute if score #rq dv.tmp matches 2 run title @a[distance=..16] actionbar {"text":"♪ Noches de neón — Santi","color":"#ff4fd8"}'))
