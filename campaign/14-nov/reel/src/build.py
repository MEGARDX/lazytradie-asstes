#!/usr/bin/env python3
"""'Every customer in November:' meme reel (Sat 14 Nov). python3 build.py → ../lazytradie-before-christmas-reel-9x16.mp4
Needs: node shoot.js first (ov/*.png). Sources: the owner's Flow/Veo clips in "14 NOv/" (9:16, 24 fps), found by their id suffix.
Full-bleed vertical, TikTok-style captions. Visible Flow watermark removed with delogo. Clip audio kept (the customers' lines are
the joke) + synthesised phone rings, record scratch and chip dings. No music: add a trending sound in Instagram."""
import os, glob, subprocess, wave, numpy as np

H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(H, '..', '..', '..', '..', '14 NOv'))
def clip(suffix): return glob.glob(os.path.join(SRC, f'*{suffix}.mp4'))[0]
RUSH, FIX, NANFARM, MUMDAD, DOORGARDEN = (clip(k) for k in ('dd2464ce', '50beda25', 'f8106861', 'dd5718b7', '96903b42'))
TMP = os.path.join(H, 'tmp'); os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(H, '..', 'lazytradie-before-christmas-reel-9x16.mp4')
VF = 'delogo=x=568:y=1128:w=66:h=66'
SR, FPS = 48000, 30

# (name, src, start, dur, [(overlay, at)], [(sfx, at)], freeze)
SEG = [
  ('ladder',  RUSH,       0.00, 2.70, [('hd1', 0.0)],                                  [('ring', 0.35)], False),
  ('door',    DOORGARDEN, 0.70, 2.30, [('hd1', 0), ('c1', 0.35)],                       [], False),
  ('garden',  DOORGARDEN, 5.15, 2.05, [('hd1', 0), ('c2', 0.35)],                       [], False),
  ('mum',     MUMDAD,     0.00, 2.60, [('hd1', 0), ('c3', 0.10)],                       [], False),
  ('pool',    MUMDAD,     5.20, 2.75, [('hd1', 0), ('c4', 0.25)],                       [], False),
  ('nan',     NANFARM,    1.00, 2.60, [('hd1', 0), ('c5', 0.30)],                       [], False),
  ('farmer',  NANFARM,    5.40, 1.90, [('hd1', 0), ('c6', 0.30)],                       [], False),
  ('twitch',  RUSH,       5.05, 2.95, [('ring', 0.2)],                                  [('ring', 0.0)], False),
  ('wait',    RUSH,       7.95, 0.70, [('wait', 0)],                                    [('scratch', 0.0)], True),
  ('calm',    FIX,        0.40, 3.90, [('hd2', 0), ('k1', 0.5), ('k2', 1.4), ('k3', 2.3)], [('ding', 0.5), ('ding', 1.4), ('ding', 2.3)], False),
  ('santa',   FIX,        5.40, 4.50, [('hd2', 0)],                                     [], False),
  ('end',     None,       0,    3.20, [('end', 0)],                                     [('ding', 0.15)], False),
]

def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode: raise SystemExit(r.stderr.decode()[-2500:])

def wav(path, x):
    x = np.clip(x, -1, 1); st = np.stack([x, x], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())

rng = np.random.default_rng(14)
def ring():   # classic Aussie double-ring: 400+450 Hz, 0.4 s on / 0.2 off / 0.4 on
    t = np.arange(int(SR * 1.0)) / SR
    tone = 0.10 * (np.sin(2 * np.pi * 400 * t) + np.sin(2 * np.pi * 450 * t)) * (np.sin(2 * np.pi * 20 * t) > -0.2)
    gate = ((t < 0.4) | ((t > 0.6) & (t < 1.0))).astype(float)
    return tone * gate
def scratch():
    d = 0.6; t = np.arange(int(SR * d)) / SR
    f = 300 + 1500 * np.abs(np.sin(2 * np.pi * 3.2 * t)) * np.exp(-t * 2); ph = 2 * np.pi * np.cumsum(f) / SR
    n = np.convolve(rng.normal(0, 1, t.size), np.ones(6) / 6, 'same')
    x = (0.22 * np.sign(np.sin(ph)) + 0.6 * n * (0.5 + 0.5 * np.sin(ph))) * np.exp(-t * 3.5); x[t > 0.42] *= 0.08
    return 0.55 * x
def ding():
    t = np.arange(int(SR * .5)) / SR
    return 0.2 * (np.sin(2 * np.pi * 1568 * t) + .6 * np.sin(2 * np.pi * 2093 * t)) * np.exp(-t * 9) * np.minimum(1, t / .004)
SFX = {'ring': ring, 'scratch': scratch, 'ding': ding}

parts = []
for i, (name, src, ss, dur, ovs, sfx, freeze) in enumerate(SEG):
    out = os.path.join(TMP, f'{i:02d}_{name}.mp4')
    n = int(SR * dur); fx = np.zeros(n)
    for kind, at in sfx:
        s = SFX[kind](); k = int(SR * at); fx[k:k + s.size] += s[:max(0, n - k)]
    fxw = os.path.join(TMP, f'{i:02d}_fx.wav'); wav(fxw, fx)
    if src is None:
        inputs = ['-f', 'lavfi', '-t', str(dur), '-i', f'color=black:s=1080x1920:r={FPS}', '-f', 'lavfi', '-t', str(dur), '-i', f'anullsrc=r={SR}:cl=stereo']
        fc = '[0:v]null[b0]'; aclip = '[1:a]'
    else:
        inputs = ['-ss', str(ss), '-t', str(dur), '-i', src]
        if freeze:
            fc = (f'[0:v]{VF},scale=1080:1920,setsar=1,trim=end_frame=1,loop=loop=60:size=1:start=0,fps={FPS},hue=s=0.15,'
                  f"zoompan=z='1+0.002*on':d=1:s=1080x1920:fps={FPS},trim=duration={dur}[b0]"); aclip = None
        else:
            fc = f'[0:v]{VF},scale=1080:1920:flags=lanczos,setsar=1,fps={FPS}[b0]'; aclip = '[0:a]'
    last = 'b0'
    for j, (ov, at) in enumerate(ovs):
        inputs += ['-loop', '1', '-t', str(dur), '-i', os.path.join(H, 'ov', ov + '.png')]; idx = inputs.count('-i') - 1
        fade = f',fade=in:st={at}:d=0.12:alpha=1' if at > 0 else ''
        fc += f';[{idx}:v]format=rgba{fade}[o{j}];[{last}][o{j}]overlay=0:0[v{j}]'; last = f'v{j}'
    fc += f';[{last}]format=yuv420p[v]'
    inputs += ['-i', fxw]; fxi = inputs.count('-i') - 1
    if aclip:
        fc += (f';{aclip}aresample={SR},aformat=channel_layouts=stereo,volume=1.4,afade=t=in:d=0.03,afade=t=out:st={dur-0.05}:d=0.05[ca]'
               f';[{fxi}:a]aresample={SR}[fx];[ca][fx]amix=inputs=2:normalize=0:duration=first[a]')
    else:
        fc += f';[{fxi}:a]aresample={SR},aformat=channel_layouts=stereo[a]'
    run(['ffmpeg', '-y'] + inputs + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', str(dur),
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-ac', '2', out])
    parts.append(out)

lst = os.path.join(TMP, 'list.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'libx264', '-crf', '20', '-maxrate', '12M', '-bufsize', '24M', '-preset', 'slow',
     '-pix_fmt', 'yuv420p', '-r', str(FPS), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-movflags', '+faststart', OUT])
print('done', OUT, round(sum(s[3] for s in SEG), 2), 's')
