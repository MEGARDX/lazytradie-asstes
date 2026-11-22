"""Loop the reference reel's own track: pass 1 + pass 2 (seamless join) + a soft tail under the end card.
python3 build_audio.py → tmp/audio.wav and prints the loop length the picture uses."""
import wave, numpy as np
from scipy import signal
SR = 48000
w = wave.open('tmp/ref.wav'); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768
L = len(a) / SR
xf = int(.015 * SR)
def join(x, y):
    r = np.linspace(0, 1, xf)[:, None]
    return np.concatenate([x[:-xf], x[-xf:] * (1 - r) + y[:xf] * r, y[xf:]])
tail = a[:int(1.45 * SR)].copy()
tail = signal.sosfilt(signal.butter(2, 1400, 'low', fs=SR, output='sos'), tail, axis=0)
tail *= np.linspace(.8, 0, len(tail))[:, None] ** 1.6
out = join(join(a, a), tail)
out = out / np.abs(out).max() * .95
with wave.open('tmp/audio.wav', 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((out * 32767).astype(np.int16).tobytes())
print('loop', round(L - xf / SR, 4), 'total', round(len(out) / SR, 3))
