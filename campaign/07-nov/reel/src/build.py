#!/usr/bin/env python3
"""Expectation vs Reality: "Day off" meme reel. python3 build.py → ../lazytradie-day-off-reel-9x16.mp4
Needs: node shoot.js first (overlay PNGs in ov/). Sources: the owner's Veo clips in "7 nov reel/" (16:9, 24 fps).
Layout: 9:16 black meme frame, the 16:9 clip at y 600–1208, captions above and below.
Audio: each clip's own sound (reality lines are Veo's dialogue), payoff shots use the same scene's ambience
(no dialogue bleed), synthesised record scratch + chip dings. No music: add the trending sound in Instagram."""
import os, subprocess, wave, numpy as np

H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(H, '..', '..', '..', '..', '7 nov reel'))
BEACH, MIX = os.path.join(SRC, 'beach.mp4'), os.path.join(SRC, 'jetty and race mix.mp4')
TMP = os.path.join(H, 'tmp'); os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(H, '..', 'lazytradie-day-off-reel-9x16.mp4')
DELOGO = 'delogo=x=1132:y=572:w=60:h=60'   # Gemini sparkle watermark, same spot in every clip
FULL, RACES = DELOGO + ',crop=1280:720:0:0', DELOGO + ',crop=1130:636:110:42'   # races shots carry a film-strip border

# (name, source, start, dur, crop, overlay, chip, audio_source_start or None)
SEG = [
  ('beach_exp',   BEACH, 0.20, 2.40, FULL,  'exp',        None,         None),
  ('beach_real',  BEACH, 3.00, 2.90, FULL,  'real_beach', None,         None),
  ('jetty_exp',   MIX,   0.40, 2.40, FULL,  'exp',        None,         None),
  ('jetty_real',  MIX,   3.30, 3.15, FULL,  'real_jetty', None,         None),
  ('races_exp',   MIX,  10.25, 2.50, RACES, 'exp',        None,         None),
  ('races_real',  MIX,  13.00, 3.35, RACES, 'real_races', None,         None),
  ('wait',        MIX,  16.30, 0.75, RACES, 'wait',       None,         'scratch'),
  ('beach_lt',    BEACH, 7.80, 2.20, FULL,  'lt_head',    'chip_beach', 0.20),
  ('jetty_lt',    MIX,   7.00, 2.30, FULL,  'lt_head',    'chip_jetty', 0.40),
  ('races_lt',    MIX,  17.20, 2.60, FULL,  'lt_head',    'chip_races', 10.25),
  ('end',         None,  0,    3.00, None,  'end',        None,         'silence'),
]
CHIP_AT = 0.35
SR = 48000

def run(cmd): subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def wav(path, x):
    x = np.clip(x, -1, 1); st = np.stack([x, x], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())

rng = np.random.default_rng(7)
def scratch(d):
    t = np.arange(int(SR * d)) / SR
    # two fast back-and-forth sweeps of filtered noise + tone = vinyl scratch, then a needle-lift thud
    f = 300 + 1500 * np.abs(np.sin(2 * np.pi * 3.2 * t)) * np.exp(-t * 2)
    ph = 2 * np.pi * np.cumsum(f) / SR
    n = rng.normal(0, 1, t.size); n = np.convolve(n, np.ones(6) / 6, 'same')
    x = (0.55 * np.sign(np.sin(ph)) * 0.4 + 0.6 * n * (0.5 + 0.5 * np.sin(ph))) * np.exp(-t * 3.5)
    x[t > 0.42] *= 0.08
    return 0.55 * x
def ding():
    t = np.arange(int(SR * .5)) / SR
    return 0.22 * (np.sin(2 * np.pi * 1568 * t) + .6 * np.sin(2 * np.pi * 2093 * t)) * np.exp(-t * 9) * np.minimum(1, t / .004)
def endtone(d):
    t = np.arange(int(SR * d)) / SR
    return 0.18 * np.sin(2 * np.pi * 55 * t) * np.exp(-t * 1.6) * np.minimum(1, t / .02) + 0.6 * ding()[:t.size].tolist().__len__() * 0 + np.pad(ding(), (0, max(0, t.size - int(SR * .5))))[:t.size]

parts = []
for i, (name, src, ss, dur, crop, ov, chip, aud) in enumerate(SEG):
    out = os.path.join(TMP, f'{i:02d}_{name}.mp4')
    ovp = os.path.join(H, 'ov', ov + '.png')
    if src is None:   # end card
        a = os.path.join(TMP, 'end.wav'); wav(a, endtone(dur))
        run(['ffmpeg', '-y', '-loop', '1', '-t', str(dur), '-i', ovp, '-i', a,
             '-filter_complex', f'[0:v]fps=30,format=yuv420p,fade=in:st=0:d=0.2[v]',
             '-map', '[v]', '-map', '1:a', '-t', str(dur), '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
             '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), out])
        parts.append(out); continue
    vin = ['-ss', str(ss), '-t', str(dur), '-i', src]
    if name == 'wait':   # freeze the last races-reality frame, desaturated, small punch-in
        vf = (f'[0:v]{crop},scale=1080:608,setsar=1,trim=end_frame=1,loop=loop=60:size=1:start=0,fps=30,'
              f'hue=s=0.15,zoompan=z=\'1+0.0025*on\':d=1:s=1080x608:fps=30,trim=duration={dur}[clip]')
    else:
        vf = f'[0:v]{crop},scale=1080:608:flags=lanczos,setsar=1,fps=30[clip]'
    fc = vf + f';color=black:s=1080x1920:r=30:d={dur}[bg];[bg][clip]overlay=0:600:shortest=1[b0];[b0][1:v]overlay=0:0[b1]'
    inputs = vin + ['-loop', '1', '-t', str(dur), '-i', ovp]
    last = 'b1'
    if chip:
        inputs += ['-loop', '1', '-t', str(dur), '-i', os.path.join(H, 'ov', chip + '.png')]
        fc += f';[2:v]format=rgba,fade=in:st={CHIP_AT}:d=0.15:alpha=1[ch];[b1][ch]overlay=0:0[b2]'; last = 'b2'
    fc += f';[{last}]format=yuv420p[v]'
    # audio
    if aud == 'scratch':
        a = os.path.join(TMP, 'scratch.wav'); wav(a, np.pad(scratch(0.6), (0, int(SR * (dur - 0.6)) + 10))[:int(SR * dur)])
        ain, amap = ['-i', a], f'{len(inputs)//2 if False else 0}'
        inputs += ['-i', a]; aidx = inputs.count('-i') - 1; af = f'[{aidx}:a]anull[a]'
    elif isinstance(aud, float):   # scene ambience from the expectation shot + chip ding
        d = os.path.join(TMP, 'ding.wav'); wav(d, np.pad(ding(), (int(SR * CHIP_AT), 0)))
        inputs += ['-ss', str(aud), '-t', str(dur), '-i', src, '-i', d]
        n = inputs.count('-i'); af = (f'[{n-2}:a]aresample={SR},volume=0.8,afade=t=in:d=0.04,afade=t=out:st={dur-0.06}:d=0.06[am];'
                                      f'[{n-1}:a]aresample={SR}[dg];[am][dg]amix=inputs=2:normalize=0:duration=first[a]')
    else:
        af = f'[0:a]aresample={SR},afade=t=in:d=0.03,afade=t=out:st={dur-0.05}:d=0.05[a]'
    run(['ffmpeg', '-y'] + inputs + ['-filter_complex', fc + ';' + af, '-map', '[v]', '-map', '[a]', '-t', str(dur),
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-ac', '2', out])
    parts.append(out)

lst = os.path.join(TMP, 'list.txt')
open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
cat = os.path.join(TMP, 'cat.mp4')
run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
     '-r', '30', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-movflags', '+faststart', OUT])
print('done', OUT, round(sum(s[3] for s in SEG), 2), 's')
