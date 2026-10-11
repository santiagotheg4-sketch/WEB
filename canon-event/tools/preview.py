"""Vista frontal rápida de modelos (ignora rotaciones). Uso: preview.py out.png body.json [head.json] ..."""
import json, sys, os
from PIL import Image
R = os.path.join(os.path.dirname(__file__), '..', 'src', 'assets')
S = 12
def tex(path):
    ns, p = path.split(':'); return Image.open(os.path.join(R, ns, 'textures', p + '.png')).convert('RGBA')
out = sys.argv[1]; files = sys.argv[2:]
W = Image.new('RGBA', (len(files) * 24 * S, 40 * S), (90, 140, 90, 255))
for k, f in enumerate(files):
    parts = f.split('+')
    for pf in parts:
        m = json.load(open(os.path.join(R, 'canon', 'models', 'modelo', pf + '.json')))
        t = tex(m['textures']['0']); ts = t.width / 16
        els = sorted(m['elements'], key=lambda e: -min(e['from'][2], e['to'][2]))
        for e in els:
            fc = e['faces'].get('north')
            if not fc: continue
            u0, v0, u1, v1 = [int(round(v * ts)) for v in fc['uv']]
            if u1 <= u0 or v1 <= v0: continue
            x0, x1 = e['from'][0], e['to'][0]; y0, y1 = e['from'][1], e['to'][1]
            w, h = int((x1 - x0) * S), int((y1 - y0) * S)
            if w <= 0 or h <= 0: continue
            img = t.crop((u0, v0, u1, v1)).resize((w, h), 0).transpose(Image.FLIP_LEFT_RIGHT)
            # vista desde el norte: x invertido
            X = k * 24 * S + int((20 - x1) * S); Y = int((24 - y1) * S)
            W.alpha_composite(img, (X, Y))
W.save(out)
