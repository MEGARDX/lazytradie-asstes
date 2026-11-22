"""Audio for each part: the reference track once (9.41 s), then a natural reverb tail of its last hits so the
end card can hold for ~3 s. python3 build_audio.py → tmp/audio.wav (both parts use the same sound)."""
import wave, numpy as np
from scipy import signal
SR = 48000; HOLD = 3.0
w = wave.open('tmp/ref.wav'); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float64) / 32768
rng = np.random.default_rng(3); n = int(3.4 * SR); t = np.arange(n) / SR
src = a[-int(.75 * SR):]                                   # the last hits + drone
out_t = []
for ch in range(2):
    ir = rng.standard_normal(n) * np.exp(-t * .75)
    ir = signal.sosfilt(signal.butter(2, 2600, 'low', fs=SR, output='sos'), ir)
    out_t.append(signal.fftconvolve(src[:, ch], ir)[len(src):len(src) + int(HOLD * SR)])
tail = np.stack(out_t, 1)
ref_rms = np.sqrt((a[-int(.1 * SR):] ** 2).mean()); tail_rms = np.sqrt((tail[:int(.1 * SR)] ** 2).mean())
tail *= ref_rms / (tail_rms + 1e-9) * .8
tail *= np.concatenate([np.ones(int(1.0 * SR)), np.linspace(1, 0, len(tail) - int(1.0 * SR)) ** 1.3])[:, None]
xf = int(.03 * SR)                                         # tail fades in under the track's last 30 ms
out = np.concatenate([a, np.zeros((len(tail) - xf, 2))])
out[len(a) - xf:] += tail * np.concatenate([np.linspace(0, 1, xf), np.ones(len(tail) - xf)])[:, None]
out = out / np.abs(out).max() * .95
with wave.open('tmp/audio.wav', 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((out * 32767).astype(np.int16).tobytes())
print('track', round(len(a) / SR, 4), 'total', round(len(out) / SR, 3))
