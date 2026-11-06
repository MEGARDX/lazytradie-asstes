"""Vision film sound: the music edit + VO + synthesised SFX, all timed from timeline.json.
python3 audio.py <outdir>  → music.wav, sfx.wav, vo.wav (48 kHz). mix.sh does the final ducked, loudness-normalised mix.
SFX are designed to sit UNDER the music: realistic, short, mostly felt rather than noticed."""
import json, os, subprocess, sys
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, 'timeline.json')))
K, DUR = TL['k'], TL['dur']
N = int(DUR * SR)
rng = np.random.default_rng(11)


def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a, r, curve=3.0):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) * curve / max(r, 1e-4))
def band(x, lo, hi):
    """FFT band-pass with soft (gaussian-ish) edges"""
    n = len(x); f = np.fft.rfftfreq(n, 1 / SR); X = np.fft.rfft(x)
    m = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, n)
def sweep_noise(d, f0, f1, bw=.7, shape=None):
    n = int(d * SR); hop, w = 512, np.hanning(2048); out = np.zeros(n + 2048); fr = np.fft.rfftfreq(2048, 1 / SR)
    for s in range(0, n, hop):
        fc = f0 * (f1 / f0) ** (s / max(n, 1)); m = np.exp(-.5 * (np.log2(np.maximum(fr, 1) / fc) / bw) ** 2)
        out[s:s + 2048] += np.fft.irfft(np.fft.rfft(rng.standard_normal(2048) * w) * m) * w
    out = out[:n] / (np.abs(out).max() + 1e-9)
    return out * (shape if shape is not None else 1)
def gliss(d, f0, f1):
    f = f0 * (f1 / f0) ** (tt(d) / max(d, 1e-6)); return np.sin(2 * np.pi * np.cumsum(f) / SR)

# ---------- instruments ----------
def whoosh(d=.8, lo=200, hi=3500, peak=.6):
    n = int(d * SR); u = np.arange(n) / n
    sh = np.where(u < peak, (u / peak) ** 2.4, np.exp(-(u - peak) / (1 - peak) * 5))
    return sweep_noise(d, lo, hi, .9, sh) * .8 + gliss(d, 90, 55) * sh * .18
def tap(f=2600, a=1.):          # glass/UI tap: two modal partials + a tiny click
    d = .5; t = tt(d); x = (np.sin(2 * np.pi * f * t) * np.exp(-t * 28) + .5 * np.sin(2 * np.pi * f * 2.71 * t) * np.exp(-t * 45))
    x[:96] += rng.standard_normal(96) * np.linspace(.6, 0, 96); return x * a * .3
def key():                       # mechanical keystroke: high click + low thock
    d = .09; t = tt(d); n = len(t)
    click = band(rng.standard_normal(n), 2500, 7000) * np.exp(-t * 180)
    thock = np.sin(2 * np.pi * (170 + rng.uniform(-20, 20)) * t) * np.exp(-t * 60)
    return (click * .5 + thock * .6) * rng.uniform(.6, 1)
def tick(): t = tt(.012); return band(rng.standard_normal(len(t)), 3000, 9000) * np.exp(-t * 500) * .35
def thud(f=60, d=.6, a=1.):
    t = tt(d); return (np.sin(2 * np.pi * np.cumsum(f * (1 + .6 * np.exp(-t * 20))) / SR) * np.exp(-t * 7) + band(rng.standard_normal(len(t)), 80, 900) * np.exp(-t * 40) * .4) * a
def boom(d=3.2):
    t = tt(d); x = np.sin(2 * np.pi * np.cumsum(58 * (1 + .8 * np.exp(-t * 6)) * np.exp(-t * .15)) / SR) * np.exp(-t * 1.2)
    x += band(rng.standard_normal(len(t)), 40, 400) * np.exp(-t * 6) * .5
    return np.tanh(x * 1.8) * .9
def riser(d=3.0):
    u = tt(d) / d; return sweep_noise(d, 300, 9000, 1.0, u ** 2.6) * .7 + gliss(d, 110, 660) * u ** 3 * .15
def ring_au():                   # Australian ring cadence (400+425 Hz), heard across a room
    d = 2.6; t = tt(d); tone = (np.sin(2 * np.pi * 400 * t) + np.sin(2 * np.pi * 425 * t)) * .5 * (.5 + .5 * np.sign(np.sin(2 * np.pi * 25 * t)))
    cad = ((t % 3.0 < .4) | ((t % 3.0 > .6) & (t % 3.0 < 1.0))).astype(float)
    return band(tone * cad, 300, 2500) * .35
def blip_down(): t = tt(.32); return (np.sin(2 * np.pi * np.where(t < .14, 880, 660) * t) * np.exp(-t * 9)) * .22
def chime():
    x = np.zeros(int(2.0 * SR))
    for j, f in enumerate([1046.5, 1318.5, 1568.0]):
        t = tt(1.6); p = (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2 * t)) * np.exp(-t * 3.5) * .25
        s = int(j * .09 * SR); x[s:s + len(p)] += p
    return x
def sparkle(d=1.2, n=26):
    x = np.zeros(int(d * SR))
    for _ in range(n):
        s = int(rng.uniform(0, d * .85) * SR); p = tap(rng.uniform(3200, 7500), rng.uniform(.15, .45)); x[s:s + len(p)] += p[:len(x) - s]
    return x
def grains(d=1.8):               # dust / crumble: dense grains thinning out
    x = np.zeros(int(d * SR))
    for i in range(900):
        u = rng.random() ** 1.8; s = int(u * d * .9 * SR); g = band(rng.standard_normal(240), 1500, 9000) * np.hanning(240) * (1 - u) * .5
        x[s:s + 240] += g[:len(x) - s]
    return x
def flutter(d=3.8):              # flag cloth: AM noise, low-passed
    t = tt(d); am = .55 + .45 * np.sin(2 * np.pi * (6.5 + 1.5 * np.sin(t * .9)) * t) ** 2
    return band(rng.standard_normal(len(t)), 120, 1600) * am * np.minimum(1, t / .6) * np.minimum(1, (d - t) / 1.2) * .35

# ---------- cue sheet ----------
L = np.zeros(N + SR * 4); R = np.zeros(N + SR * 4)
def put(x, t, g=1., pan=0.):
    s = int(t * SR); x = np.asarray(x) * g
    if s < 0: x = x[-s:]; s = 0
    gl, gr = np.sqrt((1 - pan) / 2) * 1.414, np.sqrt((1 + pan) / 2) * 1.414
    e = min(len(L), s + len(x)); L[s:e] += x[:e - s] * gl; R[s:e] += x[:e - s] * gr

V = TL['vo']
def bloom(d=4.0):                # warm major-chord swell under the orb burst (replaces the old pearl sparkle)
    t = tt(d); x = np.zeros(len(t))
    for f, g in [(110, 1), (164.8, .7), (220, .6), (277.2, .35), (329.6, .3), (440, .15)]:
        x += g * np.sin(2 * np.pi * f * t * (1 + .002 * np.sin(t * 1.3 + f)))
    return band(x, 60, 3000) * np.minimum(1, t / .5) ** 1.5 * np.exp(-t * .9) * .22
# Act 1: typing on the opening line, counters, map ticks, distant phones
txt = 'Australia was built\nby tradies.'
for i, ch in enumerate(txt):
    if ch.strip(): put(key(), V['V01'] + .05 + (K['typeEnd'] - .2 - V['V01']) * i / len(txt), .42, rng.uniform(-.25, .25))
put(whoosh(1.6, 120, 1200, .7), .1, .22)
for a, b in [(K['v02'], K['gdp'] + .3), (K['jobs'] - .7, K['jobs'] + .7), (K['biz'] - .6, K['biz'] + 1.9)]:
    tt0 = a
    while tt0 < b: put(tick(), tt0, .32, rng.uniform(-.3, .3)); tt0 += .06 + (tt0 - a) * .06
    put(tap(2000, .8), b, .4)
put(tap(2300), K['v02'] - .1, .3); put(tap(2100), K['jobs'] - .85, .3); put(tap(2500), K['small'] - .3, .3, .3)
for i in range(5): put(ring_au(), K['v04'] - .1 + i * .55, .28 * (1 - i * .12), [-.7, .5, -.2, .8, -.5][i])
# Act 2: missed notifications, the 27% hit, voicemail, the crumble, the price stack, the riser into the drop
for i, a in enumerate([K['v05'] + .6, K['v05'] + 1.7, K['v05'] + 2.8]):
    put(blip_down(), a + .15, .55, .35 - i * .2); put(whoosh(.6, 500, 4000, .5), a - .05, .14, .4)
put(thud(50, 1.0, .9), K['pct27'] - .15, .45); put(tap(1700, 1), K['pct27'] - .1, .22)
put(thud(56, .8, .7), K['pct3'] - .2, .32)
put(tap(2300, .7), K['msg'] - .05, .26); put(grains(2.6), K['goes'] + .5, .34, .2); put(whoosh(2.0, 700, 5000, .3), K['goes'] + .4, .16, .5)
for i, a in enumerate([K['v07'] + .5, K['v07'] + 1.5, K['priced'], K['big']]): put(thud(68 - i * 6, .55, .7 + i * .1), a + .4, .45); put(tap(1400 - i * 110, .6), a + .42, .22)
put(riser(3.4), K['drop'] - 3.4, .42)
# the drop: sub boom + a warm chord bloom as the orb opens
put(boom(4.0), K['drop'], .9); put(bloom(4.5), K['drop'] + .05, .8); put(whoosh(1.4, 150, 2000, .12), K['drop'], .28)
# Act 3: the phone, messages, booking chime, integrations, price card + stamps
put(whoosh(1.2, 200, 2600, .7), K['v10'] - .8, .32)
for a, p in [(K['call'], -.2), (K['text'], .1), (K['web'], .3)]: put(tap(2700, .8), a - .05, .38, p)
put(chime(), K['booked'], .45)
for i in range(4):
    pn = [-.6, .6, -.6, .6][i]; put(tap(2100 + i * 150, .7), K['tools'] + i * .4 + .35, .34, pn); put(whoosh(.6, 400, 3200, .7), K['tools'] + i * .4 - .05, .1, pn)
put(thud(46, 1.2, 1.), K['p49'] - .05, .5); put(bloom(2.5), K['p49'] - .05, .35)
for a, p, gn in [(K['setup'] - .15, -.5, .38), (K['setup'] + .8, 0, .38), (K['owned'] - .15, .5, .3)]: put(thud(88, .4, .6), a + .4, gn, p); put(tap(1900, .5), a + .42, gn * .5, p)
# Act 4: the amber wave across the map (L→R), the flag, the url
wd = max(2.4, K['grows'] - K['v13'] + .4); w = whoosh(wd, 140, 1900, .55)
for i in range(0, len(w), 4800): put(w[i:i + 4800], K['v13'] + .1 + i / SR, .36, -0.8 + 1.6 * i / len(w))
fd = K['end'] - K['v14'] - .8; put(flutter(fd), K['v14'] + .8, .5); put(bloom(4.0), K['built'] - .2, .3)
for i in range(17): put(key() * .5, K['buildAus'] + .3 + i * (1.3 / 17), .26)

# room on the SFX bus
irn = int(1.4 * SR); irt = np.arange(irn) / SR
def conv(x, h):
    m = 1 << int(np.ceil(np.log2(len(x) + len(h)))); return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(h, m), m)[:len(x)]
irL, irR = rng.standard_normal(irn) * np.exp(-irt * 4.5), rng.standard_normal(irn) * np.exp(-irt * 4.5)
wl, wr = conv(L, irL), conv(R, irR); k = np.abs(np.r_[L, R]).max() / (np.abs(np.r_[wl, wr]).max() + 1e-9)
L2, R2 = L + wl * k * .22, R + wr * k * .22; pk = max(np.abs(L2).max(), np.abs(R2).max()); L2, R2 = L2 / pk * .7, R2 / pk * .7

# VO bus
VOB = np.zeros(N + SR * 4)
for kk, t0 in V.items():
    a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(HERE, 'vo', kk + '.wav'), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                     capture_output=True).stdout, dtype=np.float32)
    s = int(t0 * SR); VOB[s:s + len(a)] += a

# music edit: [film_start, music_start, music_end] segments, equal-power crossfades (short at the intro repeat, long into the outro)
MUS = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(HERE, '..', 'assets', 'music.mp3'), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                                   capture_output=True).stdout, dtype=np.float32).reshape(-1, 2)
ML = np.zeros((N + SR * 4, 2)); SEG = TL['music']
XF = [0] + [2.0 if j == len(SEG) - 1 else .08 for j in range(1, len(SEG))]
for j, (fs, ms, me) in enumerate(SEG):
    pre, post = XF[j] / 2, (XF[j + 1] / 2 if j + 1 < len(SEG) else 0)
    a = MUS[int((ms - pre) * SR):int((me + post) * SR)].copy(); n = len(a); g = np.ones(n)
    if pre: m = int(XF[j] * SR); g[:m] = np.sin(np.linspace(0, np.pi / 2, m))
    if post: m = int(XF[j + 1] * SR); g[n - m:] = np.cos(np.linspace(0, np.pi / 2, m))
    s0 = int((fs - pre) * SR); e = min(len(ML), s0 + n); ML[s0:e] += a[:e - s0] * g[:e - s0, None]

out = sys.argv[1] if len(sys.argv) > 1 else '.'
def wav(path, ch):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', str(len(ch)), '-i', '-', path], input=np.stack(ch, 1).astype(np.float32).tobytes())
wav(os.path.join(out, 'sfx.wav'), [L2[:N], R2[:N]]); wav(os.path.join(out, 'vo.wav'), [VOB[:N]]); wav(os.path.join(out, 'music.wav'), [ML[:N, 0], ML[:N, 1]])
print('ok')
