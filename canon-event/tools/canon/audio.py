"""Sonidos sintetizados para Canon Event (numpy + scipy + espeak-ng). Todo mono, 44.1 kHz, .ogg (vorbis)."""
import os
import subprocess
import tempfile

import numpy as np
import soundfile as sf
from scipy import signal

SR = 44100
rng = np.random.default_rng(1311)


def t(sec):
    return np.arange(int(SR * sec)) / SR


def noise(sec, color='white'):
    n = rng.standard_normal(int(SR * sec))
    if color == 'pink':
        b, a = [0.049922035, -0.095993537, 0.050612699, -0.004408786], [1, -2.494956002, 2.017265875, -0.522189400]
        n = signal.lfilter(b, a, n)
    elif color == 'brown':
        n = np.cumsum(n)
        n = signal.lfilter([1, -1], [1, -0.995], n)
    return n / (np.max(np.abs(n)) + 1e-9)


def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos')
    return signal.sosfilt(sos, x)


def lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, 'lowpass', fs=SR, output='sos'), x)


def hp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, 'highpass', fs=SR, output='sos'), x)


def env(n, a, d, shape=4.0):
    e = np.ones(n)
    na, nd = int(SR * a), int(SR * d)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nd:
        e[-nd:] *= np.linspace(1, 0, nd) ** shape
    return e


def decay(n, tau):
    return np.exp(-np.arange(n) / (SR * tau))


def reson(x, f, q=30):
    b, a = signal.iirpeak(f, q, fs=SR)
    return signal.lfilter(b, a, x)


def reverb(x, size=0.6, mix=0.3):
    ir_len = int(SR * (0.3 + size * 2.2))
    ir = rng.standard_normal(ir_len) * decay(ir_len, 0.12 + size * 0.6)
    ir = lp(ir, 5000)
    wet = signal.fftconvolve(x, ir)[:len(x) + ir_len // 2]
    wet /= np.max(np.abs(wet)) + 1e-9
    out = np.zeros(len(wet))
    out[:len(x)] += x * (1 - mix)
    out += wet * mix
    return out


def norm(x, peak=0.9):
    return x / (np.max(np.abs(x)) + 1e-9) * peak


def fade(x, a=0.005, d=0.02):
    return x * env(len(x), a, d, 1.0)


def save(path, x, peak=0.9):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sf.write(path, norm(fade(x), peak).astype(np.float32), SR, format='OGG', subtype='VORBIS')


# ------------------------------------------------------------------ efectos
def paso_madera(var=0):
    n = int(SR * 0.45)
    golpe = lp(noise(0.45, 'pink'), 220) * decay(n, 0.035) * 2.2
    tabla = sum(reson(rng.standard_normal(n) * decay(n, 0.01), f, 25) * g for f, g in ((180 + var * 13, 1), (410 + var * 31, .5), (930, .2)))
    cruje = np.zeros(n)
    if var % 2:
        c = reson(noise(0.25) * env(int(SR * .25), .05, .15), 1300 + var * 90, 60) * 0.25
        cruje[int(SR * .06):int(SR * .06) + len(c)] = c
    return reverb(golpe + tabla * 0.8 + cruje, 0.25, 0.25)


def paso_tierra(var=0):
    n = int(SR * 0.35)
    x = np.zeros(n)
    for k in range(18 + var * 4):
        p = int(rng.uniform(0, 0.12) * SR)
        g = rng.standard_normal(int(SR * 0.006)) * rng.uniform(.3, 1)
        x[p:p + len(g)] += g
    x = bp(x, 900, 6000) + lp(noise(0.35, 'brown'), 120) * decay(n, 0.04) * 1.5
    return x * env(n, 0.002, 0.2)


def cruje_puerta(var=0):
    dur = 1.6 + var * 0.5
    n = int(SR * dur)
    rate = 18 + 55 * (0.5 + 0.5 * np.sin(2 * np.pi * (0.4 + var * .2) * t(dur) + var)) + rng.standard_normal(n) * 3
    ph = np.cumsum(rate / SR)
    imp = (np.diff(np.floor(ph), prepend=0) > 0).astype(float) * (0.6 + 0.4 * rng.random(n))
    x = sum(reson(imp, f, q) * g for f, q, g in ((520 + var * 40, 18, 1), (1180, 25, .7), (2300, 30, .35), (3400, 40, .15)))
    return reverb(x * env(n, 0.08, 0.35, 2), 0.4, 0.3)


def golpes(veces=3, fuerte=1.0):
    out = np.zeros(int(SR * (0.42 * veces + 0.9)))
    for k in range(veces):
        n = int(SR * 0.4)
        x = rng.standard_normal(n) * decay(n, 0.004)
        y = sum(reson(x, f, 12) * g for f, g in ((95, 1.2), (190, .9), (410, .5), (880, .2))) + lp(noise(0.4, 'brown'), 150) * decay(n, 0.05)
        p = int(SR * (k * (0.38 + rng.uniform(-.03, .05))))
        out[p:p + n] += y * fuerte * rng.uniform(.8, 1)
    return reverb(out, 0.5, 0.35)


def respiracion(lenta=True):
    dur = 4.0 if lenta else 2.4
    tt = t(dur)
    x = bp(noise(dur, 'pink'), 350, 2400)
    ciclo = 0.5 - 0.5 * np.cos(2 * np.pi * tt / (dur / 2))
    x *= ciclo ** 1.5
    x += reson(noise(dur), 900, 6) * ciclo ** 2 * 0.15
    return x


def susurro(silabas=7, var=0):
    dur = silabas * 0.16 + 0.6
    n = int(SR * dur)
    base = hp(noise(dur, 'pink'), 600)
    formantes = [(700, 1200), (400, 2200), (300, 800), (500, 1700), (650, 1000)]
    out = np.zeros(n)
    for s in range(silabas):
        f1, f2 = formantes[(s + var) % len(formantes)]
        a, b = int(SR * (0.25 + s * 0.16)), int(SR * (0.25 + s * 0.16 + 0.15))
        seg = base[a:b]
        y = reson(seg, f1 * rng.uniform(.9, 1.1), 8) + reson(seg, f2 * rng.uniform(.9, 1.1), 10) * .7 + hp(seg, 4000) * 0.25
        out[a:b] += y * np.hanning(len(seg))
    return reverb(out, 0.3, 0.2)


def latido(rapido=False):
    bpm = 120 if rapido else 68
    beat = 60 / bpm
    dur = beat * 4
    out = np.zeros(int(SR * dur))
    for k in range(4):
        for off, amp in ((0, 1.0), (0.14, 0.7)):
            n = int(SR * 0.18)
            tt = t(0.18)
            x = np.sin(2 * np.pi * (55 - 20 * tt) * tt) * decay(n, 0.05) * amp
            p = int(SR * (k * beat + off))
            out[p:p + n] += x
    return lp(out, 180)


def viento(dur=24.0):
    x = noise(dur, 'brown') * 0.6 + noise(dur, 'pink') * 0.4
    tt = t(dur)
    rafaga = 0.45 + 0.35 * np.sin(2 * np.pi * 0.07 * tt) + 0.2 * np.sin(2 * np.pi * 0.19 * tt + 1)
    y = np.zeros_like(x)
    blk = 2048
    for i in range(0, len(x), blk):
        fc = 250 + 900 * rafaga[i]
        y[i:i + blk] = x[i:i + blk]
    y = bp(y, 120, 1400) * rafaga + reson(x, 680, 3) * rafaga ** 3 * 0.2
    return loop(y)


def drone(dur=24.0, base=55.0):
    tt = t(dur)
    x = np.zeros_like(tt)
    for k, (f, g) in enumerate(((base, 1), (base * 1.498, .5), (base * 2.03, .35), (base * 0.5, .6), (base * 1.06, .3))):
        x += np.sin(2 * np.pi * f * tt + 0.3 * np.sin(2 * np.pi * (0.05 + k * .02) * tt)) * g
    x += bp(noise(dur, 'pink'), 200, 900) * (0.15 + 0.1 * np.sin(2 * np.pi * 0.03 * tt))
    x *= 0.7 + 0.3 * np.sin(2 * np.pi * 0.11 * tt)
    return loop(x)


def loop(x, xf=1.0):
    n = int(SR * xf)
    a, b = x[:n], x[-n:]
    w = np.linspace(0, 1, n)
    out = x[n:].copy()
    out[-n:] = b * (1 - w) + a * w
    return out


def persecucion(dur=16.0, bpm=128):
    tt = t(dur)
    beat = 60 / bpm
    out = np.zeros_like(tt)
    for k in range(int(dur / beat)):
        p = int(SR * k * beat)
        n = int(SR * 0.25)
        kick = np.sin(2 * np.pi * (70 - 40 * t(0.25)) * t(0.25)) * decay(n, 0.07)
        out[p:p + n] += kick[:len(out) - p] * 1.1
        if k % 2:
            hn = int(SR * 0.08)
            out[p:p + hn] += hp(noise(0.08), 5000)[:len(out[p:p + hn])] * decay(hn, 0.02) * 0.25
    cuerdas = np.zeros_like(tt)
    for f in (110, 116.5, 164.8, 233.1):
        saw = signal.sawtooth(2 * np.pi * f * tt * (1 + 0.003 * np.sin(2 * np.pi * 5 * tt)))
        cuerdas += saw
    cuerdas = lp(cuerdas, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * (bpm / 60 / 4) * tt) ** 2) * 0.35
    golpes_met = np.zeros_like(tt)
    for k in range(0, int(dur / beat), 8):
        p = int(SR * k * beat)
        n = int(SR * 1.2)
        m = sum(reson(rng.standard_normal(n) * decay(n, 0.003), f, 80) for f in (523, 1187, 1960)) * decay(n, 0.4)
        golpes_met[p:p + n] += m[:len(golpes_met) - p] * 0.3
    return loop(reverb(out + cuerdas + golpes_met, 0.35, 0.2)[:len(tt)], 0.5)


def stinger():
    dur = 2.5
    tt = t(dur)
    x = sum(np.sin(2 * np.pi * f * (1 + 0.02 * tt) * tt) for f in (233, 247, 311, 466, 494))
    x = x * env(len(tt), 0.05, 1.6, 2) + hp(noise(dur), 3000) * decay(len(tt), 0.3) * 0.5
    return reverb(x, 0.7, 0.4)


def lluvia_estatica(dur=3.0):
    return bp(noise(dur), 800, 7000) * (0.6 + 0.4 * (rng.random(int(SR * dur)) > 0.97))


def guitarra_triste(dur=8.0):
    """Rasgueo desafinado (Santiago canta «Mari no contesta»)."""
    out = np.zeros(int(SR * dur))
    acordes = [(196, 247, 294), (165, 196, 247), (175, 220, 262), (147, 185, 220)]
    for k in range(int(dur / 1.0)):
        ac = acordes[k % 4]
        for j, f in enumerate(ac):
            n = int(SR * 1.6)
            p = int(SR * (k * 1.0 + j * 0.025))
            ks = karplus(f * rng.uniform(0.99, 1.012), 1.6)
            out[p:p + n] += ks[:max(0, min(n, len(out) - p))] * 0.5
    return reverb(out, 0.3, 0.2)


def karplus(f, dur):
    n = int(SR * dur)
    L = int(SR / f)
    buf = rng.uniform(-1, 1, L)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % L]
        buf[i % L] = 0.996 * 0.5 * (buf[i % L] + buf[(i + 1) % L])
    return out


def silbido(cerca=True):
    """El Silbón: silbido que sube (do-re-mi-fa-sol-la-si). Lejos suena fuerte y seco; cerca suena débil y con eco."""
    notas = [523, 587, 659, 698, 784, 880, 988]
    out = []
    for f in notas:
        tt = t(0.32)
        x = np.sin(2 * np.pi * f * tt * (1 + 0.004 * np.sin(2 * np.pi * 6 * tt))) * env(len(tt), 0.04, 0.12)
        x += bp(noise(0.32), f * 0.9, f * 1.1) * 0.15
        out.append(x)
    x = np.concatenate(out)
    return reverb(x, 0.9 if cerca else 0.15, 0.6 if cerca else 0.1)


def voz(texto, grave=True, eco=True, voice='es+m3'):
    """Voz de computador en español, distorsionada para que dé miedo."""
    with tempfile.TemporaryDirectory() as d:
        w = os.path.join(d, 'v.wav')
        subprocess.run(['espeak-ng', '-v', voice, '-s', '125', '-p', '20' if grave else '70', '-w', w, texto], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        x, sr = sf.read(w)
    if x.ndim > 1:
        x = x.mean(axis=1)
    x = signal.resample(x, int(len(x) * SR / sr))
    if grave:
        x = signal.resample(x, int(len(x) * 1.18))  # más lenta y grave
    x = x + 0.25 * np.tanh(x * 6)  # ronquera
    x = bp(x, 120, 5200)
    x += hp(noise(len(x) / SR), 3000) * 0.04 * np.abs(signal.hilbert(x))  # aire
    return reverb(x, 0.5, 0.35) if eco else x
