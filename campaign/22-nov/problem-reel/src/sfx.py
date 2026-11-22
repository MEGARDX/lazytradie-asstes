"""Sound-design kit for the 22 Nov reel: designed (not beepy) UI and Foley-style cues, 48 kHz mono float arrays.
Each cue is band-limited, enveloped and later sent through a short stereo room so it sits in the music instead of on top."""
import numpy as np
from scipy import signal

SR = 48000
rng = np.random.default_rng(2211)


def tt(d): return np.arange(int(d * SR)) / SR
def n_(d): return int(d * SR)
def bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'high', fs=SR, output='sos'), x)
def env(d, a, r, curve=4.0):
    t = tt(d); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) * curve / max(r, 1e-4))
def norm(x, g=1.0): return x / (np.abs(x).max() + 1e-9) * g
def gliss(d, f0, f1, curve='exp'):
    t = tt(d) / d; f = f0 * (f1 / f0) ** t if curve == 'exp' else f0 + (f1 - f0) * t
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def sweep_noise(d, f0, f1, q=1.5, shape=None):
    """pink-ish noise through a band-pass whose centre glides f0→f1 (time-varying via short blocks)"""
    n = n_(d); out = np.zeros(n); blk = 256; x = rng.standard_normal(n + blk)
    zi = None; fc_prev = None
    for s in range(0, n, blk):
        fc = f0 * (f1 / f0) ** (s / max(n, 1))
        lo, hi = fc / (1 + 1 / q), min(fc * (1 + 1 / q), SR / 2 - 100)
        sos = signal.butter(2, [lo, hi], 'band', fs=SR, output='sos')
        if zi is None: zi = signal.sosfilt_zi(sos) * 0
        y, zi = signal.sosfilt(sos, x[s:s + blk], zi=zi)
        out[s:s + blk] = y[:len(out[s:s + blk])]
    out = norm(out)
    return out * (shape if shape is not None else 1)


# ---------- cues ----------
def vibrate(d=0.34, g=1.0):
    """phone buzzing on a hard surface: ~170 Hz motor, soft-clipped, with surface rattle"""
    t = tt(d); m = np.sin(2 * np.pi * 172 * t + 0.6 * np.sin(2 * np.pi * 9 * t))
    body = np.tanh(3.2 * m) * (0.75 + 0.25 * np.sin(2 * np.pi * 31 * t))
    rattle = bp(rng.standard_normal(len(t)), 900, 3200) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 172 * t))) * 0.25
    e = np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.04)
    return lp(body * 0.7 + rattle, 4000) * e * 0.5 * g


def ringback(d=2.0):
    """Australian ringback (400+425/450 Hz, 0.4 on, 0.2 off, 0.4 on, 2 off) heard down a phone line"""
    t = tt(d); x = (np.sin(2 * np.pi * 400 * t) + np.sin(2 * np.pi * 450 * t)) * 0.5
    gate = ((t % 3.0 < 0.4) | ((t % 3.0 > 0.6) & (t % 3.0 < 1.0))).astype(float)
    gate = np.convolve(gate, np.ones(240) / 240, 'same')
    return bp(np.tanh(1.5 * x) * gate, 300, 3400, 3) * 0.16


def hangup():
    """two soft line-drop tones"""
    x = np.zeros(n_(0.5))
    for j, f in enumerate((480, 380)):
        s = n_(j * 0.17); p = np.sin(2 * np.pi * f * tt(0.13)) * env(0.13, 0.005, 0.13, 2)
        x[s:s + len(p)] += p
    return bp(x, 300, 3400) * 0.22


def click(g=1.0, bright=1.0):
    """crisp UI click: two-layer transient (top tick + small body)"""
    d = 0.045; t = tt(d)
    top = hp(rng.standard_normal(len(t)), 2500 * bright) * np.exp(-t * 600)
    body = np.sin(2 * np.pi * 1450 * bright * t) * np.exp(-t * 180) * 0.5
    low = np.sin(2 * np.pi * 220 * t) * np.exp(-t * 90) * 0.35
    return (top * 0.35 + body + low) * 0.32 * g


def key(g=1.0):
    """keyboard key: plastic tick + thock, randomised"""
    d = 0.07; t = tt(d); f = rng.uniform(1800, 2600)
    tick_ = bp(rng.standard_normal(len(t)), f, f * 1.6) * np.exp(-t * 420)
    thock = np.sin(2 * np.pi * rng.uniform(140, 190) * t) * np.exp(-t * 70) * 0.5
    return (norm(tick_) * 0.6 + thock) * 0.16 * g * rng.uniform(0.8, 1.1)


def pop(g=1.0, f=620):
    """soft bubble pop: short upward-bending sine with a breathy edge"""
    d = 0.16; t = tt(d)
    x = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.9 * (1 - np.exp(-t * 40)))) / SR) * env(d, 0.003, 0.16, 6)
    air = bp(rng.standard_normal(len(t)), 2000, 7000) * np.exp(-t * 120) * 0.15
    return (x + air) * 0.22 * g


def swish(d=0.42, up=True, g=1.0):
    """airy pass-by whoosh"""
    n = n_(d); u = np.linspace(0, 1, n); sh = np.where(u < 0.55, (u / 0.55) ** 2, np.exp(-(u - 0.55) / 0.45 * 5))
    x = sweep_noise(d, 380, 4200, 1.2, sh) if up else sweep_noise(d, 4200, 380, 1.2, sh)
    return x * 0.16 * g


def thunk(g=1.0):
    """item landing in a plastic wheelie bin: hollow body + paper slap"""
    d = 0.5; t = tt(d)
    body = (np.sin(2 * np.pi * 105 * t) + 0.5 * np.sin(2 * np.pi * 168 * t)) * np.exp(-t * 14)
    slap = bp(rng.standard_normal(len(t)), 500, 2600) * np.exp(-t * 60) * 0.6
    return lp(body * 0.8 + slap, 3000) * 0.3 * g


def coin(g=1.0):
    """coin clink: inharmonic metal partials, a little random detune each time"""
    d = 0.6; t = tt(d); x = np.zeros(len(t)); base = rng.uniform(2300, 2700)
    for m, a, dec in ((1, 1, 9), (1.53, .7, 11), (2.31, .45, 14), (3.07, .3, 18), (4.12, .2, 24)):
        x += a * np.sin(2 * np.pi * base * m * t + rng.uniform(0, 6)) * np.exp(-t * dec)
    x[n_(0.05):] += 0.5 * x[:len(x) - n_(0.05)] * 0.5      # second bounce
    return x * np.minimum(1, t / 0.0015) * 0.07 * g


def slam(g=1.0):
    """bin lid slam: plastic crack + low thump"""
    d = 0.7; t = tt(d)
    crack = lp(rng.standard_normal(len(t)), 1800) * np.exp(-t * 45)
    thump = gliss(d, 95, 55) * np.exp(-t * 9)
    return np.tanh((norm(crack) * 0.7 + thump) * 1.4) * 0.42 * g


def tock(g=1.0, f=1900):
    """clock tick: woody, short"""
    d = 0.05; t = tt(d)
    x = bp(rng.standard_normal(len(t)), f, f * 1.5) * np.exp(-t * 300) + np.sin(2 * np.pi * 900 * t) * np.exp(-t * 220) * 0.3
    return norm(x) * 0.08 * g


def scribble(d=0.5, g=1.0):
    """marker drawing a circle on glass"""
    t = tt(d); fm = 2600 + 900 * np.sin(2 * np.pi * (1 / d) * t)
    x = bp(rng.standard_normal(len(t)), 1800, 6000) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 7 * t)))
    squeak = np.sin(2 * np.pi * np.cumsum(fm) / SR) * 0.08
    e = np.sin(np.pi * t / d) ** 0.7
    return (norm(x) * 0.5 + squeak) * e * 0.12 * g


def bell(f=1318, d=1.6, g=1.0):
    """glassy FM bell"""
    t = tt(d); idx = 2.2 * np.exp(-t * 6)
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.5 * t)) * np.exp(-t * 3.2)
    x += 0.3 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t * 5)
    return x * np.minimum(1, t / 0.002) * 0.1 * g


def chime(g=1.0, root=1047):
    """soft three-note confirm"""
    x = np.zeros(n_(1.9))
    for j, m in enumerate((1, 1.25, 1.5)):
        p = bell(root * m, 1.5, 1.0 - j * 0.15); s = n_(j * 0.07); x[s:s + len(p)] += p
    return x * g


def ratchet(d=0.36, g=1.0):
    """slot-machine spin: accelerating then slowing ticks"""
    x = np.zeros(n_(d + 0.05)); tcur = 0.0; k = 0
    while tcur < d:
        p = click(0.5, 1.4); s = n_(tcur); x[s:s + len(p)] += p[:len(x) - s]
        k += 1; tcur += 0.018 + 0.05 * (tcur / d) ** 2
    return x * g


def sub_boom(d=2.4, g=1.0):
    """drop impact: sub glide + body knock + air"""
    t = tt(d)
    sub = gliss(d, 58, 32) * np.exp(-t * 1.6)
    knock = gliss(0.3, 160, 60) * env(0.3, 0.002, 0.3, 6)
    air = sweep_noise(0.9, 5000, 600, 1.0, env(0.9, 0.003, 0.9, 5)) * 0.35
    x = sub * 0.9; x[:len(knock)] += knock * 0.6; x[:len(air)] += air
    return np.tanh(x * 1.5) * 0.55 * g


def reverse_swell(d=1.6, g=1.0):
    """reverse cymbal-ish swell into a hit"""
    t = tt(d); u = t / d
    x = hp(rng.standard_normal(len(t)), 3000) * u ** 3
    tone = (np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 330 * t)) * u ** 4 * 0.15
    return (norm(x) * 0.6 + tone) * 0.22 * g


def riser(d=2.0, g=1.0):
    u = tt(d) / d
    return (sweep_noise(d, 300, 7000, 1.4, u ** 2.4) * 0.6 + gliss(d, 110, 440) * u ** 3 * 0.18) * 0.3 * g


def shimmer(d=0.8, g=1.0):
    x = sweep_noise(d, 6000, 9000, 2.0, env(d, d * 0.3, d * 0.7, 3)) * 0.2
    for _ in range(9):
        s = n_(rng.uniform(0, d * 0.7)); p = bell(rng.uniform(2600, 5200), 0.5, rng.uniform(.25, .5)); x[s:s + len(p)] += p[:len(x) - s]
    return x * g


def low_hit(g=1.0):
    """muted downbeat hit for statements"""
    d = 1.2; t = tt(d)
    x = gliss(d, 70, 42) * np.exp(-t * 4) + lp(rng.standard_normal(len(t)), 400) * np.exp(-t * 18) * 0.3
    return np.tanh(x * 1.3) * 0.35 * g


def swoosh_send(g=1.0):
    """message 'sent' swoosh"""
    d = 0.32; u = np.linspace(0, 1, n_(d)); sh = np.sin(np.pi * u) ** 2
    return (sweep_noise(d, 900, 5000, 2.0, sh) * 0.5 + gliss(d, 600, 1400) * sh * 0.12) * 0.22 * g


def room(L, R, wet=0.18, t60=0.9):
    """short decorrelated stereo room"""
    n = n_(t60); t = np.arange(n) / SR
    irl = rng.standard_normal(n) * np.exp(-t * 6.9 / t60); irr = rng.standard_normal(n) * np.exp(-t * 6.9 / t60)
    irl, irr = lp(irl, 6000), lp(irr, 6000)
    wl, wr = signal.fftconvolve(L, irl)[:len(L)], signal.fftconvolve(R, irr)[:len(R)]
    s = max(np.abs(wl).max(), np.abs(wr).max()) / (max(np.abs(L).max(), np.abs(R).max()) + 1e-9)
    return L + wl / s * wet, R + wr / s * wet
