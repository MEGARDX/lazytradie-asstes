#!/usr/bin/env python3
"""Problem → solution explainer reel: asset prep. python3 prep.py
 1. Beat-locked timeline: 115.05 BPM (beat 0.5215 s). Music enters at track 13.574 s so the drum drop (track 50.079 s)
    lands on reel 36.505 s = scene 14 "Meet LazyTradie". Every scene is a whole number of beats.
 2. Clip frames (30 fps JPEG) cropped so the Gemini/Flow ✦ watermark (bottom-right, ~x600 y1160 of 720×1280) is cut out:
    card clips use a 4:5 window above it; full-bleed clips crop the bottom edge. Lanczos upscale + light sharpen.
 3. VO word timings (faster-whisper) → kinetic captions in timeline.js.
 4. Audio: music (ducked under VO) + the 20 VO lines + synthesised SFX on the beat → tmp/mix.wav.
"""
import os, json, glob, subprocess, wave
import numpy as np

H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(H, '..', '..', '..', '..'))
ASSET = os.path.join(ROOT, 'Uploads', '19 Nov', 'Reel 11 nov')
NOV14 = os.path.join(ROOT, '14 NOv')
NOV17 = os.path.join(ROOT, '17 nov')
FR = os.path.join(H, 'frames'); TMP = os.path.join(H, 'tmp')
os.makedirs(FR, exist_ok=True); os.makedirs(TMP, exist_ok=True)
def clip(folder, key): return glob.glob(os.path.join(folder, f'*{key}*.mp4'))[0]
C_PHONE, C_WOMAN, C_DAD, C_LAPTOP, C_TRUCK = (clip(ASSET, k) for k in ('eb079b8a', '605d9bb6', '7143895d', '2c3c0f1c', 'd13edaf2'))
C_LADDER, C_CALM = clip(NOV14, 'dd2464ce'), clip(NOV14, '50beda25')
MUSIC = os.path.join(ASSET, 'atlasaudio-sci-fi-ambient-587603.mp3')
BEAT, M_IN = 0.5215, 0.015 + 26 * 0.5215          # reel 0 = track beat 26
FPS, SR = 30, 48000

TXT = {  # on-screen words; *…* = italic serif accent
 1: "Your phone's *ringing.*", 2: "You're up a *ladder.*", 3: "She doesn't leave a *message.*", 4: "She calls the *next tradie.*",
 5: "He texts for a *quote.*", 6: "Two hours *later,* you reply.", 7: "He's already booked *someone else.*", 8: "She asks your *website.*",
 9: "It says, *“we'll get back to you.”*", 10: "Every enquiry that waits is *money in the bin.*", 11: "Customers don't *wait* anymore.",
 12: "You know you're losing them. You just don't know *how to fix it.*", 13: "That's where *we come in.*", 14: "Meet *LazyTradie.*",
 15: "Every call, text and website chat, answered *instantly.*", 16: "Jobs booked straight into *your calendar.*",
 17: "Big jobs wait for *your OK.*", 18: "Every call log and transcript, *in one place.*", 19: "You stay *on the tools.*",
 20: "LazyTradie. Stress about work, *not bookings.*"}
BEATS = {1: 6, 2: 4, 3: 4, 4: 4, 5: 6, 6: 6, 7: 5, 8: 4, 9: 6, 10: 9, 11: 5, 12: 7, 13: 4,
         14: 5, 15: 9, 16: 6, 17: 5, 18: 8, 19: 5, 20: 12}
LEAD = {1: 2 * BEAT, 14: 0.35, 20: 0.3}
# scene clip frame jobs: scene -> (src, start, mode)  mode 'card' (4:5 crop at y0) or 'full'
CLIPS = {1: (C_PHONE, 1.0, ('full',)), 2: (C_LADDER, 0.2, ('card', 0)), 3: (C_WOMAN, 0.9, ('card', 110)), 4: (C_WOMAN, 4.0, ('card', 110)),
         5: (C_DAD, 0.4, ('card', 190)), 8: (C_LAPTOP, 1.4, ('card', 210)), 9: (C_LAPTOP, 4.6, ('card', 210)),
         12: (C_TRUCK, 0.4, ('full',)), 19: (C_CALM, 0.3, ('card', 0))}

def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode: raise SystemExit(r.stderr.decode()[-2000:])

# ---- timeline ----
scenes, t = [], 0.0
for n in range(1, 21):
    d = round(BEATS[n] * BEAT, 4)
    vo = os.path.join(ASSET, f'{n:02d}.wav')
    scenes.append({'n': n, 'start': round(t, 4), 'dur': d, 'vo': vo, 'voStart': round(t + LEAD.get(n, 0.2), 4), 'text': TXT[n]})
    t += d
TOTAL = round(t, 4)
assert abs(scenes[13]['start'] - (50.079 - M_IN)) < 0.01, scenes[13]['start']

AUDIO_ONLY = os.environ.get('AUDIO_ONLY') == '1'   # AUDIO_ONLY=1 python3 prep.py → re-mix sound only
if AUDIO_ONLY:
    _tl = open(os.path.join(H, 'timeline.js')).read(); meta = json.loads(_tl[_tl.index('{'):_tl.rindex('}') + 1])
    for sc, old in zip(scenes, meta['scenes']): sc.update(old)
else:
    # ---- VO word timings ----
    from faster_whisper import WhisperModel
    wm = WhisperModel('small.en', device='cpu', compute_type='int8')
    def pcm16k(f):
        return np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                                            capture_output=True).stdout, dtype=np.int16).astype(np.float32) / 32768
    for sc in scenes:
        segs, _ = wm.transcribe(pcm16k(sc['vo']), word_timestamps=True)
        ws = [w for s in segs for w in s.words]
        toks = sc['text'].split(' ')
        if len(ws) == len(toks): times = [(w.start, w.end) for w in ws]
        else:  # spread evenly over the spoken span
            a, b = (ws[0].start, ws[-1].end) if ws else (0, 1.5); step = (b - a) / len(toks)
            times = [(a + i * step, a + (i + 1) * step) for i in range(len(toks))]
        sc['words'] = [{'w': tok, 't': round(sc['voStart'] + tt[0], 3)} for tok, tt in zip(toks, times)]
        sc['voEnd'] = round(sc['voStart'] + (ws[-1].end if ws else 1.5), 3)

    # ---- clip frames ----
    for n, (src, ss, mode) in CLIPS.items():
        sc = scenes[n - 1]; out = os.path.join(FR, f's{n:02d}'); os.makedirs(out, exist_ok=True)
        for f in glob.glob(out + '/*.jpg'): os.remove(f)
        dur = sc['dur'] + 0.3
        if mode[0] == 'card':
            vf = f'crop=720:900:0:{mode[1]},scale=800:1000:flags=lanczos,unsharp=5:5:0.6,fps={FPS}'
        else:  # full-bleed: drop the bottom strip that holds the watermark, keep 9:16
            vf = 'crop=630:1120:45:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.7,fps=30'
        run(['ffmpeg', '-y', '-ss', str(ss), '-t', str(dur), '-i', src, '-vf', vf, '-q:v', '3', os.path.join(out, '%04d.jpg')])
    # stills for scene 11 (customers drifting away) + campaign photo cards for scene 19
    for name, (src, ss, y0) in {'w': (C_WOMAN, 2.0, 110), 'd': (C_DAD, 1.5, 190), 'l': (C_LAPTOP, 3.0, 210)}.items():
        run(['ffmpeg', '-y', '-ss', str(ss), '-i', src, '-frames:v', '1', '-vf', f'crop=720:900:0:{y0},scale=640:800:flags=lanczos', '-q:v', '3',
             os.path.join(FR, f'still_{name}.jpg')])
    from PIL import Image
    for name, path in {'camp1': os.path.join(NOV14, 'Gemini_Generated_Image_63ezkl63ezkl63ez.png'),
                       'camp2': os.path.join(NOV17, '1.png'), 'camp3': os.path.join(NOV17, '2.png')}.items():
        im = Image.open(path).convert('RGB'); W, Hh = im.size; ch = int(W * 1.25)
        im.crop((0, max(0, (Hh - ch) // 2 - 80), W, max(0, (Hh - ch) // 2 - 80) + ch)).resize((640, 800), Image.LANCZOS).save(os.path.join(FR, f'{name}.jpg'), quality=90)

    meta = {'fps': FPS, 'beat': BEAT, 'total': TOTAL, 'drop': scenes[13]['start'], 'scenes': [{k: v for k, v in s.items() if k != 'vo'} for s in scenes],
            'frames': {f's{n:02d}': len(glob.glob(os.path.join(FR, f's{n:02d}', '*.jpg'))) for n in CLIPS}}
    open(os.path.join(H, 'timeline.js'), 'w').write('window.TL = ' + json.dumps(meta, ensure_ascii=False) + ';\n')

# ---- audio ----
n = int(SR * (TOTAL + 0.6)); rng = np.random.default_rng(22)
def tt(d): return np.arange(int(SR * d)) / SR
def add(buf, x, at, g=1.0):
    i = int(SR * at); j = min(len(buf), i + len(x)); buf[i:j] += g * x[:j - i]
def load(f):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                                     capture_output=True).stdout, dtype=np.int16).astype(np.float32) / 32768
    return a
def buzz(d=0.32):
    x = tt(d); return 0.22 * np.sign(np.sin(2 * np.pi * 150 * x)) * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * x)) * np.minimum(1, x / .01) * np.minimum(1, (d - x) / .03)
def whoosh(d=0.45):
    x = tt(d); nz = np.convolve(rng.normal(0, 1, x.size), np.ones(18) / 18, 'same')
    env = np.sin(np.pi * x / d) ** 2; return 0.10 * nz * env
def pop():
    x = tt(0.12); return 0.16 * np.sin(2 * np.pi * (900 - 2500 * x) * x) * np.exp(-x * 35)
def chime(f=1568):
    x = tt(0.7); return 0.12 * (np.sin(2 * np.pi * f * x) + .5 * np.sin(2 * np.pi * f * 1.5 * x)) * np.exp(-x * 6) * np.minimum(1, x / .004)
def tick():
    x = tt(0.05); return 0.09 * np.sin(2 * np.pi * 2600 * x) * np.exp(-x * 90)
def clink():
    x = tt(0.35); return 0.13 * sum(np.sin(2 * np.pi * f * x) * np.exp(-x * k) for f, k in ((2350, 14), (3720, 18), (5100, 24))) * np.minimum(1, x / .002)
def thud():
    x = tt(0.4); return 0.35 * np.sin(2 * np.pi * (70 - 30 * x) * x) * np.exp(-x * 9)
def key():
    x = tt(0.04); return 0.07 * rng.normal(0, 1, x.size) * np.exp(-x * 120)
def ringback():
    x = tt(1.0); g = ((x < 0.4) | ((x > 0.6) & (x < 1.0))).astype(float)
    return 0.05 * (np.sin(2 * np.pi * 400 * x) + np.sin(2 * np.pi * 450 * x)) * g
def riser(d):
    x = tt(d); f = 200 + 1600 * (x / d) ** 2; ph = 2 * np.pi * np.cumsum(f) / SR
    nz = np.convolve(rng.normal(0, 1, x.size), np.ones(8) / 8, 'same')
    return (0.05 * np.sin(ph) + 0.10 * nz) * (x / d) ** 2
def impact():
    x = tt(1.6); return 0.5 * np.sin(2 * np.pi * (55 - 20 * x) * x) * np.exp(-x * 3.5) + 0.08 * rng.normal(0, 1, x.size) * np.exp(-x * 7)

sfx = np.zeros(n); vo = np.zeros(n); wl = np.zeros(n); wr = np.zeros(n)
S = {s['n']: s for s in scenes}
for s in scenes:
    add(vo, load(os.path.join(ASSET, f"{s['n']:02d}.wav")), s['voStart'], 1.0)
    if s['n'] not in (1, 14):
        w_ = whoosh(); pan = np.linspace(0.15, 0.85, w_.size)
        if s['n'] % 2: pan = pan[::-1]
        add(wl, w_ * np.sqrt(1 - pan), s['start'] - 0.18, 1.1); add(wr, w_ * np.sqrt(pan), s['start'] - 0.18, 1.1)
b = lambda sn, k: S[sn]['start'] + k * BEAT
for k in range(6): add(sfx, buzz(), b(1, k))
for k in range(4): add(sfx, buzz(), b(2, k), 0.6)
add(sfx, ringback(), b(3, 0.4)); add(sfx, thud(), b(3, 3.3), 0.6)
add(sfx, whoosh(0.35), b(4, 2), 0.9); add(sfx, clink(), b(4, 3)); add(sfx, thud(), b(4, 3.1), 0.5)
for k in range(14): add(sfx, key(), b(5, 2) + k * 0.11)
add(sfx, whoosh(0.3), b(5, 5), 0.8)
for k in range(24): add(sfx, tick(), b(6, 0) + k * BEAT / 4)
add(sfx, pop(), b(7, 1.6)); add(sfx, clink(), b(7, 3.6)); add(sfx, thud(), b(7, 3.7), 0.5)
for k in range(10): add(sfx, key(), b(8, 0.5) + k * 0.1)
add(sfx, pop(), b(8, 3)); add(sfx, chime(990), b(9, 1), 0.7)
for k in range(9):
    add(sfx, clink(), b(10, k) + 0.05); add(sfx, clink(), b(10, k) + BEAT / 2, 0.6)
add(sfx, thud(), b(10, 8.6), 0.9)
add(sfx, thud(), b(11, 0), 0.8)
for k in (1, 2, 3): add(sfx, pop(), b(12, k), 0.4)   # notifications stack up
add(sfx, riser(S[13]['dur'] + 0.05), S[13]['start'])
add(sfx, impact(), S[14]['start']); add(sfx, chime(1318), b(14, 1), 0.8)
for k in (1, 2.5, 4):  # chips land with the words call / text / website; ✓ half a beat later; chime on "instantly"
    add(sfx, pop(), b(15, k)); add(sfx, tick(), b(15, k + 0.5), 1.2)
add(sfx, chime(1568), b(15, 7), 0.8)
for k in (2, 3, 4): add(sfx, pop(), b(16, k), 0.8)
add(sfx, tick(), b(17, 2.7)); add(sfx, chime(1760), b(17, 3), 0.9)
for k in (1, 2, 3, 4): add(sfx, tick(), b(18, k))
for k in (4.5, 5.5, 6.5): add(sfx, pop(), b(18, k), 0.45)   # transcript bubbles
for k in (1, 2, 3): add(sfx, whoosh(0.3), b(19, k), 0.7)
add(sfx, chime(1318), b(20, 0)); add(sfx, pop(), b(20, 8), 0.8); add(sfx, chime(1975), b(20, 8.5), 0.7)   # CTA after the last line

mus2 = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', MUSIC, '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'],
                                    capture_output=True).stdout, dtype=np.int16).astype(np.float32).reshape(-1, 2) / 32768
mus2 = mus2[int(SR * M_IN):int(SR * M_IN) + n]; mus2 = np.pad(mus2, ((0, max(0, n - len(mus2))), (0, 0)))
mus2 = mus2 / (np.sqrt((mus2[int(SR * 40):int(SR * 55)] ** 2).mean()) + 1e-9) * 0.10    # level the drop section
g = np.full(n, 1.0)
for s in scenes:  # duck under VO with 120 ms ramps
    a, z = int(SR * (s['voStart'] - 0.12)), int(SR * (s['voEnd'] + 0.15))
    g[max(0, a):z] = np.minimum(g[max(0, a):z], 0.55)
g = np.convolve(g, np.ones(int(SR * 0.12)) / int(SR * 0.12), 'same')
fade = np.ones(n); fo = int(SR * 2.2); fade[-fo:] = np.linspace(1, 0, fo); fade[:int(SR * .4)] = np.linspace(0, 1, int(SR * .4))
c = vo * 1.0 + sfx * 0.9
mix = np.stack([c + mus2[:, 0] * g * fade + wl * 0.9, c + mus2[:, 1] * g * fade + wr * 0.9], 1)
mix = mix / max(1e-9, np.abs(mix).max()) * 0.95
with wave.open(os.path.join(TMP, 'mix.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('total', TOTAL, 'drop at', scenes[13]['start'], 'frames', meta['frames'], 'stereo mix written')
