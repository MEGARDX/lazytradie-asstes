"""10 s demo: place VO lines 01-05 back to back, get word timings (faster-whisper), mix a quiet music bed.
python3 prep.py → timeline.js + tmp/audio.wav"""
import os, json, subprocess, wave, numpy as np
from faster_whisper import WhisperModel
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
VO = os.path.join(ROOT, 'Uploads', '19 Nov', 'Reel 11 nov'); MUS = os.path.join(VO, 'atlasaudio-sci-fi-ambient-587603.mp3')
SR = 48000
def load(f, ch=1):
    return np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', str(ch), '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout, dtype=np.int16).astype(np.float32).reshape(-1, ch) / 32768
TXT = {1: "Your phone's ringing.", 2: "You're up a ladder.", 3: "She doesn't leave a message.", 4: "She calls the next tradie.", 5: "He texts for a quote."}
wm = WhisperModel('small.en', device='cpu', compute_type='int8')
t, lines, vo = 0.35, [], []
for n in range(1, 6):
    a = load(os.path.join(VO, f'{n:02d}.wav'))[:, 0]
    segs, _ = wm.transcribe(load(os.path.join(VO, f'{n:02d}.wav'))[::3, 0], word_timestamps=True)
    ws = [w for s in segs for w in s.words]; toks = TXT[n].split()
    if len(ws) == len(toks): times = [w.start for w in ws]
    else: a0, a1 = (ws[0].start, ws[-1].end) if ws else (0, len(a) / SR); times = [a0 + i * (a1 - a0) / len(toks) for i in range(len(toks))]
    end = (ws[-1].end if ws else len(a) / SR)
    lines.append({'n': n, 'start': round(t, 3), 'end': round(t + end, 3), 'words': [{'w': w, 't': round(t + x, 3)} for w, x in zip(toks, times)]})
    vo.append((t, a)); t += len(a) / SR + 0.12
TOTAL = round(max(10.0, t + 0.6), 3)
n = int(TOTAL * SR); mix = np.zeros((n, 2))
for t0, a in vo: i = int(t0 * SR); mix[i:i + len(a)] += a[:n - i, None]
m = load(MUS, 2)[int(40 * SR):int(40 * SR) + n]; m = np.pad(m, ((0, n - len(m)), (0, 0)))
m = m / (np.sqrt((m ** 2).mean()) + 1e-9) * 0.035
fade = np.ones(n); fade[:int(.5 * SR)] = np.linspace(0, 1, int(.5 * SR)); fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR))
mix += m * fade[:, None]; mix = mix / np.abs(mix).max() * .95
with wave.open('tmp/audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
open('timeline.js', 'w').write('window.TL = ' + json.dumps({'total': TOTAL, 'lines': lines}) + ';\n')
print('total', TOTAL); [print(l['n'], l['start'], l['end'], [w['w'] for w in l['words']]) for l in lines]
