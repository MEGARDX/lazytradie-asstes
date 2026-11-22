#!/usr/bin/env python3
"""Problem → solution explainer reel: asset prep. python3 prep.py
 1. Beat-locked timeline: 115.05 BPM (beat 0.5215 s). Music enters at track 13.574 s so the drum drop (track 50.079 s)
    lands on reel 36.505 s = scene 14 "Meet LazyTradie". Every scene is a whole number of beats.
 2. Clip frames (30 fps JPEG) cropped so the Gemini/Flow ✦ watermark (bottom-right, ~x600 y1160 of 720×1280) is cut out:
    card clips use a 4:5 window above it; full-bleed clips crop the bottom edge. Lanczos upscale + light sharpen.
 3. VO word timings (faster-whisper) → kinetic captions in timeline.js.
 4. Audio: music (ducked under VO) + the 20 VO lines + designed SFX (sfx.py) on each animation event → tmp/mix.wav.
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
# Sound design v2: every cue is placed on the animation event it belongs to (same beat maths as reel.html: bt(n, k)).
# Cues come from sfx.py (designed, band-limited, through a short stereo room) and sit ~10 dB under the voice.
import sfx as X
n = int(SR * (TOTAL + 0.6))
S = {s['n']: s for s in scenes}
b = lambda sn, k: S[sn]['start'] + k * BEAT
DROP = S[14]['start']
L = np.zeros(n); Rr = np.zeros(n); vo = np.zeros(n)
def put(x, at, g=1.0, pan=0.0):
    i = int(SR * at)
    if i < 0: x = x[-i:]; i = 0
    j = min(n, i + len(x)); seg = x[:j - i] * g
    L[i:j] += seg * np.sqrt((1 - pan) / 2) * 1.414; Rr[i:j] += seg * np.sqrt((1 + pan) / 2) * 1.414
def load(f):
    return np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                                        capture_output=True).stdout, dtype=np.int16).astype(np.float32) / 32768
for s in scenes:
    a = load(os.path.join(ASSET, f"{s['n']:02d}.wav")); i = int(SR * s['voStart']); vo[i:i + len(a)] += a[:n - i]

# S1 phone buzzing on the dash; mono labels tick on
for k in range(1, 6): put(X.vibrate(), b(1, k), .6, -0.15)
for k in (2, 3, 4): put(X.click(.5, 1.3), b(1, k), 1, 0.3)
put(X.swish(.5, False), S[2]['start'] - .34, .8)                       # pull-back into the card
# S2 still buzzing, further away
for k in range(4): put(X.lp(X.vibrate(), 1800), b(2, k), .35, -0.1)
# S3 her side of the line: ringback, then the line drops and the marker circles it
put(X.click(.6), b(3, .2)); put(X.ringback(3.0 * BEAT), b(3, .3), 1.0, 0.1)
put(X.hangup(), b(3, 3.3), 1.0); put(X.scribble(.5), b(3, 3.35), 1.0, 0.1)
# S4 call 1 → call 2, the bin rolls in, her job goes in the bin
put(X.pop(.55, 520), b(4, .4), 1, -0.4); put(X.swish(.3), b(4, 1.0), .35); put(X.pop(.8, 700), b(4, 1.9), 1, 0.3)
put(X.low_hit(.35), b(4, 1.5), 1, 0.5); put(X.swish(.42), b(4, 2), .55, 0.4)
put(X.thunk(), b(4, 3), 1, 0.6); put(X.slam(.45), b(4, 3.12), 1, 0.6)
# S5 he types (a chip per word), the words drop into the field, sent
for i in range(8):
    t0 = b(5, 2) + i * (2.9 * BEAT / 8)
    for j in range(2 + (i % 2)): put(X.key(), t0 + j * .055, 1, -0.1 + .05 * j)
put(X.swish(.3), b(5, 4.95), .4); put(X.swoosh_send(), b(5, 5.1), 1, 0.2); put(X.pop(.6, 760), b(5, 5.35), 1, 0.1)
put(X.swish(.55, True), S[6]['start'] - .32, .9); put(X.low_hit(.4), S[6]['start'], 1)  # zoom-through
# S6 the clock runs two hours in 24 ticks
for k in range(24): put(X.tock(1.0, 1900 if k % 2 else 1600), b(6, 0) + k * BEAT / 4, .9, -0.2 + .4 * (k % 2))
put(X.pop(.6, 640), b(6, 4), 1)
# S7 his reply; the quote goes in the bin
put(X.pop(.5, 560), b(7, .1)); put(X.swish(.42), b(7, 2.6), .55, 0.4); put(X.thunk(), b(7, 3.6), 1, 0.6); put(X.slam(.4), b(7, 3.72), 1, 0.6)
# S8 the website form: typing, cursor, annotation arrow, click
for k in range(12): put(X.key(.8), b(8, .5) + k * .085, 1, -0.2)
put(X.swish(.25, True), b(8, 1.8), .3, 0.4); put(X.pop(.5, 580), b(8, 2.2), 1, -0.3); put(X.click(1.0, .9), b(8, 3), 1, 0.3)
# S9 the auto-reply, then the marker circles "48 hours"
put(X.chime(.55, 880), b(9, 1), 1); put(X.scribble(.55), b(9, 3), 1, -0.1)
put(X.swish(.45, False), S[10]['start'] - .25, .7)
# S10 the bin eats the week: an item lands on every beat, a coin on every off-beat, lid slams shut
for k in range(9):
    put(X.thunk(.9), b(10, k) + .05, 1, -0.3 + .6 * (k % 2)); put(X.coin(.8), b(10, k) + BEAT / 2, 1, 0.3 - .6 * (k % 2))
put(X.slam(1.0), b(10, 8.6), 1)
# S11 statement + text cloud
put(X.low_hit(1.0), b(11, 0)); put(X.swish(1.2, True), b(11, .5), .25)
# S12 notifications stack up
for k in (1, 2, 3): put(X.pop(.55, 600 + 60 * k), b(12, k), 1, -0.3)
# S13 → drop: riser, reverse swell, iris opens on the sub boom
put(X.riser(S[13]['dur'] + .05), S[13]['start'], .9); put(X.reverse_swell(1.2), DROP - 1.2, .8)
put(X.sub_boom(1.0), DROP); put(X.shimmer(.9, .6), DROP + .05)
# S14 labels tick on, the wordmark reveals with the VO
for k in (.3, .6, .9, 1.2): put(X.click(.4, 1.4), b(14, k), 1, (-1) ** int(k * 10) * .4)
put(X.swish(.45, True), b(14, 1.6), .5); put(X.bell(1318, 1.6, .6), S[14]['words'][1]['t'] if 'words' in S[14] else b(14, 1.75))
# S15 slot carousel spins onto Calls / Texts / Web chats; pills pop; "instantly"
put(X.swish(.4), S[15]['start'] - .15, .5)
for k in (1, 2.5, 4): put(X.ratchet(.36), b(15, k) - .36, 1); put(X.click(.9, 1.1), b(15, k), 1)
for k in (1.5, 3, 4.5): put(X.pop(.6, 700), b(15, k), 1, 0.2)
put(X.chime(.8, 1047), b(15, 7), 1)
# S16 the sky tilts down into the sunset; checks tick; jobs drop into the calendar
put(X.swish(.6, False), S[16]['start'] - .3, .7)
for k in (1.5, 2.5, 3.5): put(X.click(.6, 1.2), b(16, k), 1, -0.4)
for k in (2, 3, 4): put(X.pop(.7, 660), b(16, k), 1, 0.3)
# S17 arrow, tap, approved, toast
put(X.pop(.5, 560), b(17, 1.5), 1, -0.3); put(X.click(1.0, .9), b(17, 2.7), 1, 0.3); put(X.chime(.9, 1175), b(17, 3), 1); put(X.pop(.6, 760), b(17, 3.3))
# S18 rows tick in, transcript bubbles pop, marker circles the booking
for k in (1, 2, 3, 4): put(X.click(.5, 1.2), b(18, k), 1, 0.3)
for k in (4.5, 5.5, 6.5): put(X.pop(.5, 620), b(18, k), 1, -0.2 if k != 5.5 else 0.3)
put(X.scribble(.5), b(18, 5), 1, 0.3)
# S19 the deck fans out; S20 collapse into the lockup
for k, pn in ((1, -0.5), (2, 0.5), (3, 0)): put(X.swish(.4), b(19, k) - .12, .55, pn)
put(X.swish(.45, False), S[20]['start'] - .35, .6)
put(X.chime(.8, 1047), b(20, 0)); put(X.pop(.7, 640), b(20, 8), 1, -0.3); put(X.pop(.6, 700), b(20, 8.12), 1, 0.3)
put(X.chime(.6, 1318), b(20, 8.5)); put(X.click(.4, 1.3), b(20, 9.5))

L, Rr = X.room(L * .8, Rr * .8, .2, .9)   # SFX bus sits ~2 dB lower
mus2 = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', MUSIC, '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'],
                                    capture_output=True).stdout, dtype=np.int16).astype(np.float32).reshape(-1, 2) / 32768
mus2 = mus2[int(SR * M_IN):int(SR * M_IN) + n]; mus2 = np.pad(mus2, ((0, max(0, n - len(mus2))), (0, 0)))
mus2 = mus2 / (np.sqrt((mus2[int(SR * 40):int(SR * 55)] ** 2).mean()) + 1e-9) * 0.10    # level the drop section
g = np.full(n, 1.0)
for s in scenes:  # duck under VO
    a, z = int(SR * (s['voStart'] - 0.12)), int(SR * (s['voEnd'] + 0.15))
    g[max(0, a):z] = np.minimum(g[max(0, a):z], 0.55)
g = np.convolve(g, np.ones(int(SR * 0.12)) / int(SR * 0.12), 'same')
fade = np.ones(n); fo = int(SR * 2.2); fade[-fo:] = np.linspace(1, 0, fo); fade[:int(SR * .4)] = np.linspace(0, 1, int(SR * .4))
rms = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
act = lambda x: x[np.abs(x) > 1e-3] if (np.abs(x) > 1e-3).any() else x
print('active RMS  vo %.1f dB  sfx %.1f dB' % (rms(act(vo)), rms(act((L + Rr) / 2))))
mix = np.stack([vo + mus2[:, 0] * g * fade + L, vo + mus2[:, 1] * g * fade + Rr], 1)
mix = mix / max(1e-9, np.abs(mix).max()) * 0.95
with wave.open(os.path.join(TMP, 'mix.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('total', TOTAL, 'drop at', DROP, 'stereo mix written')
