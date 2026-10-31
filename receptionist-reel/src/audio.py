"""Sound for the AI Receptionist reel: places the VO and synthesises every SFX cue from timeline.json.
python3 audio.py <outdir>  ->  vo.wav, sfx.wav (48 kHz stereo float). The final mix is done with ffmpeg."""
import json, os, subprocess, sys
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, 'timeline.json')))
K, DUR = TL['k'], TL['dur']
N = int(DUR * SR) + SR
rng = np.random.default_rng(7)


def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a, r, curve=3.0):
    """attack seconds a, then exponential-ish release over r seconds"""
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) * curve / max(r, 1e-4))
    return e


def bandnoise(d, f0, f1, bw=0.6, shape=None):
    """noise whose passband sweeps f0 -> f1 (log), via overlap-add FFT chunks"""
    n = int(d * SR); hop = 512; win = np.hanning(2048); out = np.zeros(n + 2048)
    fr = np.fft.rfftfreq(2048, 1 / SR)
    for i, s in enumerate(range(0, n, hop)):
        u = s / max(n, 1); fc = f0 * (f1 / f0) ** u
        mask = np.exp(-0.5 * (np.log2(np.maximum(fr, 1) / fc) / bw) ** 2)
        x = rng.standard_normal(2048) * win
        out[s:s + 2048] += np.fft.irfft(np.fft.rfft(x) * mask) * win
    out = out[:n]; out /= (np.abs(out).max() + 1e-9)
    return out * (shape if shape is not None else 1)


def gliss(d, f0, f1):
    f = f0 * (f1 / f0) ** (tt(d) / d); return np.sin(2 * np.pi * np.cumsum(f) / SR)


def whoosh(d=0.7, up=True, peak=0.62, lo=250, hi=4200):
    n = int(d * SR); t = np.arange(n) / n
    sh = np.where(t < peak, (t / peak) ** 2.2, np.exp(-(t - peak) / (1 - peak) * 4))
    x = bandnoise(d, lo, hi, 0.8, sh) if up else bandnoise(d, hi, lo, 0.8, sh)
    return x * 0.8 + gliss(d, 70, 45) * sh * 0.25


def boom(d=2.2, f0=62, f1=30, big=1.0):
    x = gliss(d, f0, f1) * env(int(d * SR), 0.004, d, 3.2)
    k = gliss(0.35, 140, 60) * env(int(0.35 * SR), 0.002, 0.35, 5) * 0.6
    x[:len(k)] += k
    nz = bandnoise(0.25, 900, 120, 1.2, env(int(0.25 * SR), 0.001, 0.25, 7)) * 0.5
    x[:len(nz)] += nz
    return np.tanh(x * 1.6 * big) * 0.9


def ping(f=2200, d=1.4, a=1.0):
    n = int(d * SR); t = tt(d); x = np.zeros(n)
    for m, amp, dec in [(1, 1, 1.0), (2.76, .45, .55), (5.4, .22, .3), (8.93, .1, .2)]:
        x += amp * np.sin(2 * np.pi * f * m * t) * np.exp(-t / (dec * d / 3))
    return x * env(n, 0.002, d, 0.01) * a * 0.35


def tick(f=3200, a=1.0):
    n = int(0.03 * SR); t = tt(0.03)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 260) + rng.standard_normal(n) * np.exp(-t * 900) * .3) * a * .45


def shimmer(d=0.9, a=1.0):
    x = bandnoise(d, 5000, 9000, 0.5, env(int(d * SR), d * .4, d * .6, 3)) * .25
    for _ in range(14):
        s = int(rng.uniform(0, d * .8) * SR); p = ping(rng.uniform(3000, 7000), .5, rng.uniform(.15, .35))
        x[s:s + len(p)] += p[:len(x) - s]
    return x * a


def swell(d=2.0, f=44, a=1.0):
    n = int(d * SR); t = np.arange(n) / n
    sh = np.sin(np.pi * t) ** 1.5
    return (np.sin(2 * np.pi * f * tt(d)) * .7 + bandnoise(d, 90, 160, 0.7) * .4) * sh * a


def riser(d=1.3):
    n = int(d * SR); t = np.arange(n) / n
    return (bandnoise(d, 500, 9000, 0.9, t ** 2.5) * .7 + gliss(d, 180, 900) * t ** 3 * .2)


def ring():
    """soft modern ring: alternating glass notes, twice"""
    x = np.zeros(int(1.3 * SR))
    for burst in (0, 0.62):
        for j in range(5):
            p = ping([1318, 1661][j % 2], .5, .55); s = int((burst + j * .075) * SR); x[s:s + len(p)] += p[:len(x) - s]
    return x


def chime():
    x = np.zeros(int(2.2 * SR))
    for j, f in enumerate([1047, 1319, 1568, 2093]):
        p = ping(f, 1.8, .9); s = int(j * .085 * SR); x[s:s + len(p)] += p
    return x


def shutter():
    n = int(.12 * SR)
    x = bandnoise(.12, 2500, 5000, 0.6, env(n, .001, .05, 6)) * .5
    x = x + np.sin(2 * np.pi * 85 * tt(.12))[:n] * env(n, .001, .12, 6) * .7
    return x


def alert():
    x = np.zeros(int(1.2 * SR))
    for j, f in enumerate([1480, 1109, 1480, 1109]):
        p = ping(f, .45, .8); s = int(j * .14 * SR); x[s:s + len(p)] += p
    x[:int(.6 * SR)] += np.sin(2 * np.pi * 55 * tt(.6)) * env(int(.6 * SR), .01, .6, 4) * .5
    return x


# ---------- cue sheet ----------
L = np.zeros(N); R = np.zeros(N)
def put(x, t, g=1.0, pan=0.0):
    s = int(t * SR)
    if s >= N: return
    x = x[:N - s] * g
    L[s:s + len(x)] += x * np.sqrt((1 - pan) / 2) * 1.414
    R[s:s + len(x)] += x * np.sqrt((1 + pan) / 2) * 1.414

put(swell(2.6, 41, .5), 0.0)
put(shimmer(.9, .5), 0.2)
put(whoosh(.5, True, .7, 300, 3000), K['bars'] - .3, .45, -.6); put(whoosh(.5, True, .7, 300, 3000), K['bars'] - .3, .45, .6)
put(whoosh(.55, False), K['conv'], .5)
put(boom(1.8, 70, 34, .8), K['icon'], .75); put(ping(1760, 1.6, .7), K['icon'] + .02, .6)
put(whoosh(.6, True, .5, 400, 6000), K['iconOut'], .5)
put(tick(2400, .8), K['pill']); put(riser(.4), K['pill'], .25)
put(ping(2637, 1.0, .5), K['btn'], .5)
for k, p in (('cd1', -.4), ('cd2', 0), ('cd3', .4)):
    put(whoosh(.55, True, .7, 350, 3800), K[k] - .3, .45, p); put(tick(2800, .8), K[k] + .3, .6, p)
put(swell(2.2, 38, 1.0), K['orb'] - .2, .9); put(boom(2.6, 52, 28, .6), K['orb'], .55); put(shimmer(1.2, .7), K['orb'] + .1, .6)
put(whoosh(.5, False, .55, 300, 5000), K['orbOut'] - .1, .5)
put(ping(2093, .8, .6), K['chip'] + .05, .55, -.5)
put(gliss(.25, 600, 2400) * env(int(.25 * SR), .01, .25, 4) * .2, K['branch'], 1, -.2)
for k, f, p in (('b1', 880, .3), ('b2', 1175, .4), ('b3', 1397, .5)):
    put(whoosh(.45, True, .4, 600, 6000), K[k] - .15, .4, p); put(ping(f, 1.0, .7), K[k] + .05, .55, p)
for i in range(17): put(tick(3600 + (i % 3) * 300, .5), K['name'] + i * .04, .5, -.5)
for i in range(3): put(ping(2349, .7, .45), K['ans'] + i * .28 + .1, .5, .45)
put(whoosh(.7, False, .5, 200, 2500), K['dim'], .35)
put(whoosh(.6, False), K['chipOut'], .5)
put(tick(2000, .6), K['ghost'] + .05)
put(ring(), K['lit'] + .03, .75)
put(whoosh(.55, True, .6, 300, 5000), K['card'] - .2, .5); put(ping(1568, 1.2, .6), K['card'] + .2, .5)
for k in ('s1', 's2', 's3', 's4'): put(tick(3000, .7), K[k] + .05, .6, .2)
put(ping(2637, 1.2, .9), K['booked'] + .02, .7); put(ping(3951, 1.0, .5), K['booked'] + .08, .5)
put(whoosh(.5, False, .6, 300, 5000), K['drop'] - .2, .55)
put(riser(.5), K['grad'] - .5, .35); put(boom(2.6, 58, 30, 1.0), K['grad'], .85); put(swell(3.0, 46, .6), K['grad'], .6)
put(chime(), K['bk'] + .05, .8); put(shimmer(1.0, .5), K['bk'], .5)
put(ping(1976, 1.0, .6), K['cal'] + .05, .55)
put(whoosh(.6, True, .6, 300, 6000), K['bkOut'], .55)
put(whoosh(.6, True, .7), K['side'] - .15, .5, -.6)
put(tick(2600, .9), K['hl'] + .05, .7, -.4)
put(whoosh(.6, True, .7), K['jobs'] - .15, .5, .5)
for i in range(5): put(tick(2900 + i * 120, .6), K['detail'] - .45 + i * .14, .55, .3)
put(whoosh(.6, False, .5, 200, 3000), K['dashOut'], .45)
put(shimmer(1.0, .7), K['tiers'], .6); put(swell(1.8, 40, .6), K['tiers'] - .2, .6)
put(whoosh(.6, True, .5, 400, 6000), K['tiersOut'], .45)
put(swell(4.5, 36, .8), K['car'], .7); put(whoosh(.9, True, .7, 200, 2000), K['car'] - .2, .4)
put(ping(1568, 1.2, .7), K['t1'], .55); put(ping(1175, 1.2, .7), K['t2'], .55)
put(whoosh(.5, False), K['carOut'] - .05, .5)
per = (K['wipe'] + .2 - K['mont']) / 6
for i in range(6): put(shutter(), K['mont'] + i * per, .8, (-1) ** i * .3)
put(alert(), K['emerg'] + .05, .65)
put(riser(1.0), K['slam'] - 1.0, .5); put(whoosh(.7, True, .65, 300, 7000), K['wipe'], .6)
put(boom(3.2, 60, 27, 1.3), K['slam'], 1.0); put(shimmer(1.2, .6), K['slam'] + .05, .5)
put(whoosh(.8, False, .5, 200, 3000), K['frame'] - .1, .4); put(swell(3.0, 44, .6), K['frame'], .6)
put(shimmer(1.4, .7), K['wm'], .6); put(ping(2093, 1.6, .6), K['wm'] + .1, .45)
put(ping(2637, 1.6, .9), K['price'] + .02, .7); put(ping(3520, 1.2, .5), K['price'] + .1, .5)
put(shimmer(1.0, .5), K['never'], .5)
for i in range(17): put(tick(3400 + (i % 4) * 200, .5), K['url'] + i * (1.0 / 17), .5)
put(swell(4.0, 40, .7), DUR - 4.2, .6)

# room: short stereo reverb on the SFX bus
ir_n = int(1.6 * SR); irt = np.arange(ir_n) / SR
irL = rng.standard_normal(ir_n) * np.exp(-irt * 4.2); irR = rng.standard_normal(ir_n) * np.exp(-irt * 4.2)
def conv(x, h):
    m = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(h, m), m)[:len(x)]
wl, wr = conv(L, irL), conv(R, irR); sc = np.abs(np.concatenate([wl, wr])).max() / (np.abs(np.concatenate([L, R])).max() + 1e-9)
L2, R2 = L + wl / sc * .28, R + wr / sc * .28
pk = max(np.abs(L2).max(), np.abs(R2).max()); L2, R2 = L2 / pk * .7, R2 / pk * .7

# VO bus
V = np.zeros(N)
for k, t0 in TL['vo'].items():
    f = [x for x in os.listdir(os.path.join(HERE, '../assets/vo')) if x.startswith(k)][0]
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(HERE, '../assets/vo', f), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32); s = int(t0 * SR); V[s:s + len(a)] += a[:N - s]

out = sys.argv[1] if len(sys.argv) > 1 else '.'
def wav(path, ch):
    d = np.stack(ch, 1).astype(np.float32)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', str(len(ch)), '-i', '-', path], input=d.tobytes())
n = int(DUR * SR)
wav(os.path.join(out, 'sfx.wav'), [L2[:n], R2[:n]]); wav(os.path.join(out, 'vo.wav'), [V[:n]])
print('ok', n / SR)
