"""Vision film VO prep: trim long in-line pauses to 0.22 s, speed up ×TEMPO (pitch kept), write vo/Vxx.wav.
python3 vo_prep.py <voice dir> <words.json from whisper>"""
import json, os, subprocess, sys
import numpy as np
SR, TEMPO, KEEP = 48000, 1.0, 0.55
SRC = {'V01': 'V01.mp3', 'V02': 'V02.mp3', 'V03': 'V03.mp3', 'V04': 'V04.mp3', 'V05': 'V05.mp3', 'V06': 'V06.mp3',
       'V07': 'V07.mp3', 'V08': 'V08.mp3', 'V09': 'V09.mp3', 'V10': 'V10.mp3', 'V11': 'v11 (works with the tools).mp3',
       'V12': 'V12 for just 49.mp3', 'V13': 'V13.mp3', 'V14': 'V14.mp3'}
vdir, W = sys.argv[1], json.load(open(sys.argv[2]))
here = os.path.dirname(os.path.abspath(__file__))
for k, f in SRC.items():
    a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(vdir, f), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                     capture_output=True).stdout, dtype=np.float32)
    # cut only real silence: 10 ms RMS frames below -38 dB of the line's peak, runs > 0.32 s shrink to KEEP
    fr = int(0.01 * SR); n = len(a) // fr
    rms = np.sqrt((a[:n * fr].reshape(n, fr) ** 2).mean(1) + 1e-12); db = 20 * np.log10(rms / rms.max())
    loud = np.where(db > -38)[0]; first, last = loud[0], loud[-1]
    parts, cur, i = [], max(0, first - 4) * fr, first
    while i <= last:
        if db[i] <= -38:
            j = i
            while j <= last and db[j] <= -38: j += 1
            if (j - i) * 0.01 > 0.75:
                parts.append(a[cur:(i * fr + int(KEEP / 2 * SR))]); cur = j * fr - int(KEEP / 2 * SR)
            i = j
        else: i += 1
    parts.append(a[cur:min(len(a), (last + 18) * fr)])
    out = np.concatenate(parts)
    fade = int(0.01 * SR); out[:fade] *= np.linspace(0, 1, fade); out[-fade:] *= np.linspace(1, 0, fade)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', f'atempo={TEMPO}' if TEMPO != 1 else 'anull',
                    os.path.join(here, 'vo', k + '.wav')], input=out.astype(np.float32).tobytes())
    print(k, round(len(out) / SR / TEMPO, 2))
