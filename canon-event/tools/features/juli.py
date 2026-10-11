from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon.models import *  # noqa: F401,F403
import random, json

def models_juli():
    at = Atlas('juli', 31)
    skin = '#ecd2bf'
    grey = '#7c7378'

    def shirt_paint(a, f, r):
        x, y, w, h = r
        if f == 'north':
            # hombro descubierto (blusa off-shoulder) + collar plateado con dije
            rect(a, x, y, int(w * 0.38), 4, skin)
            rect(a, x + int(w * 0.38), y, w - int(w * 0.38), 1, shade(hexc(grey), 0.8))
            cx = x + w // 2
            for t in range(0, 6):
                px(a, cx - 3 + t, y + 1 + (t if t < 3 else 5 - t), '#d9d9de')
            rect(a, cx - 1, y + 5, 2, 2, '#f4f4f8')
            # pliegues suaves
            for i in range(0, w, 5):
                for j in range(6, h):
                    if (i + j) % 7 == 0:
                        px(a, x + i, y + j, shade(hexc(grey), 0.85))
        if f == 'up':
            rect(a, x, y, w, h, skin)

    def arm_paint(a, f, r):
        # mangas largas holgadas, la mano asoma
        x, y, w, h = r
        rect(a, x, y + h - 3, w, 3, skin)
        rect(a, x, y + h - 5, w, 1, '#c9a46a')  # pulsera

    def skirt_paint(a, f, r):
        x, y, w, h = r
        for i in range(0, w, 3):
            for j in range(h):
                px(a, x + i, y + j, '#0d0d10')

    def leg_paint(a, f, r):
        x, y, w, h = r
        for i in range(w):
            for j in range(h):
                if (i * 3 + j) % 5 == 0:
                    px(a, x + i, y + j, '#26222a')

    c = dict(skin=skin, pants='#2f2a33', shoes='#5b3f2c', boots=True, belt='#1a1a1e', shirt=grey, sleeve=grey,
             skirt='#1b1b20', skirt_paint=skirt_paint, leg_paint=leg_paint, shirt_paint=shirt_paint,
             arm_paint=arm_paint, arm_w=2.5, wide_shoulders=0.2)
    P = humanoid_parts(at, c)
    for n, cmdn in [('idle', 'idle'), ('walk_a', 'walk_a'), ('walk_b', 'walk_b'), ('reach', 'reach'), ('float', 'float')]:
        write_model('juli_' + n, 'juli', pose(P, cmdn))
    at.save()
    ah = Atlas('juli_cabeza', 32)
    hair = '#3a261d'
    H = head_parts(ah, dict(skin=skin, hair=hair), 'bob')
    base = dict(iris='#2b1a12', brow='#2a1a14', lips='#c06a72', blush='#e7b0aa')
    exprs = {
        'smile': dict(base, mouth='smile'),
        'soft': dict(base, mouth='smile', eyes='closed'),
        'sad': dict(base, mouth='frown', tears=True),
        'surprised': dict(base, mouth='o'),
    }
    for n, st in exprs.items():
        r = face_rect(ah)
        fe = face_element(ah, r, skin, st, 'face_' + n)
        write_model('juli_cabeza_' + n, 'juli_cabeza', all_elements(H) + [fe])
    ah.save()






def build(c):
    shim.use(c)
    # Juli 2.1: reemplaza los modelos base (mismos nombres y CMD 7320094..7320102)
    from canon import skins as SK
    SK.build_character('juli', dict(skin='#ecd2bf', hair='#3a261d', hair_style='bob', eyes='#2b1a12', top='#7c7378', top_style='blouse',
                                    pants='#1b1b20', pants_style='skirt', tights='#2f2a33', shoes='#5b3f2c', lips='#c06a72',
                                    extras=['necklace', 'blush']), c.out,
                       ('idle', 'walk_a', 'walk_b', 'reach', 'float'),
                       [('smile', 'smile'), ('soft', 'soft'), ('sad', 'cry'), ('surprised', 'surprised')])
