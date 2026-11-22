"""One continuous build, no mid restart: the reference track plays up to its fast section, that section
(three hits, ~0.29 s apart) is looped on the hits, then the track's own ending lands the logo.
python3 build_audio.py → tmp/audio.wav + cuts.js (the cut times the picture uses)."""
import wave, json, numpy as np
from scipy import signal
SR = 48000
w = wave.open('tmp/ref.wav'); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768
A, B = 7.512, 8.383            # loop the hits at 7.517 / 7.813 / 8.102 (cut 5 ms before each transient)
K = 6                          # 6 loops = 18 extra hits
REF = [0, .733, 1.4, 2.0, 2.533, 3.033, 3.5, 3.967, 4.367, 4.733, 5.167, 5.533, 5.9, 6.233, 6.567, 6.9, 7.2, 7.5, 7.8, 8.033]   # reference cuts up to B
HITS = [.005, .301, .590]      # hit offsets inside the loop
i = lambda t: int(round(t * SR)); xf = i(.008)
def join(x, y):
    r = np.linspace(0, 1, xf)[:, None]; return np.concatenate([x[:-xf], x[-xf:] * (1 - r) + y[:xf] * r, y[xf:]])
seg = a[i(A):i(B)]; out = a[:i(B)]
for _ in range(K): out = join(out, seg)
out = join(out, a[i(B):])
SEG = (i(B) - i(A) - xf) / SR
E = B + K * SEG - xf / SR      # where the track's own ending (hit 8.388) resumes
tail = signal.sosfilt(signal.butter(2, 1400, 'low', fs=SR, output='sos'), a[:i(1.45)].copy(), axis=0) * np.linspace(.8, 0, i(1.45))[:, None] ** 1.6
end_len = len(out) / SR
out = join(out, tail); out = out / np.abs(out).max() * .95
with wave.open('tmp/audio.wav', 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((out * 32767).astype(np.int16).tobytes())
cuts = REF + [round(B + k * SEG + h, 4) for k in range(K) for h in HITS] + [round(E + .005, 4), round(E + .308, 4)]
meta = {'cuts': cuts, 'logo': round(E + .549, 4), 'cta': round(E + .831, 4), 'end': round(len(out) / SR, 4)}
open('cuts.js', 'w').write('window.CUTS = ' + json.dumps(meta) + ';\n')
print(len(cuts), 'cuts · logo', meta['logo'], '· cta', meta['cta'], '· total', meta['end'])
