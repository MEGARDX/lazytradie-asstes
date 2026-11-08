#!/usr/bin/env python3
"""'Tradies at 8pm on a Sunday' meme reel. python3 build.py → ../lazytradie-sunday-8pm-reel-9x16.mp4
Needs: node shoot.js first (overlay PNGs in ov/). Sources: the owner's Veo clips "8 nov/1.mp4" (horror) and "8 nov/2.mp4" (twist), 16:9, 24 fps.
Layout: 9:16 black meme frame, clip at y 600–1208, captions above/below. Gemini sparkle watermark removed with delogo.
Audio: each clip's own sound + synthesised horror sting, record scratch and chip dings. No music: add the trending sound in Instagram."""
import os, subprocess, wave, numpy as np

H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(H, '..', '..', '..', '..', '8 nov'))
C1, C2 = os.path.join(SRC, '1.mp4'), os.path.join(SRC, '2.mp4')
TMP = os.path.join(H, 'tmp'); os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(H, '..', 'lazytradie-sunday-8pm-reel-9x16.mp4')
VF = 'delogo=x=1132:y=572:w=60:h=60'
SR = 48000

# (name, src, start, dur, [(overlay, appear_at)], sfx list [(kind, at)], freeze)
SEG = [
  ('couch',   C1, 0.00, 2.90, [('head1', 0)],                              [],                    False),
  ('turn',    C1, 2.98, 3.42, [('head1', 0)],                              [],                    False),
  ('table',   C1, 6.48, 3.50, [('head1', 0), ('cap_wait', 0.9)],           [('sting', 0.0)],      False),
  ('wait',    C1, 9.90, 0.75, [('wait', 0)],                               [('scratch', 0.0)],    True),
  ('quote',   C2, 0.00, 3.98, [('head2', 0), ('cap_quote', 0.25)],         [],                    False),
  ('draft',   C2, 4.04, 2.42, [('head2', 0), ('chip_draft', 0.3)],         [('ding', 0.3)],       False),
  ('cheer',   C2, 6.54, 3.46, [('head2', 0), ('chip_sent', 0.35)],         [('ding', 0.35)],      False),
  ('end',     None, 0,  3.20, [('end', 0)],                                [('ding', 0.15)],      False),
]

def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode: raise SystemExit(r.stderr.decode()[-2500:])

def wav(path, x):
    x = np.clip(x, -1, 1); st = np.stack([x, x], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())

rng = np.random.default_rng(8)
def sting():   # horror hit: sub boom + dissonant detuned stab + noise swell
    d = 2.2; t = np.arange(int(SR * d)) / SR
    boom = np.sin(2 * np.pi * (48 - 14 * t) * t) * np.exp(-t * 2.2)
    stab = sum(np.sign(np.sin(2 * np.pi * f * t)) * 0.18 for f in (233.1, 246.9, 349.2, 370.0)) * np.exp(-t * 3.0)
    n = np.convolve(rng.normal(0, 1, t.size), np.ones(40) / 40, 'same') * np.exp(-t * 1.5)
    return 0.55 * boom + 0.22 * stab + 0.35 * n
def scratch():
    d = 0.6; t = np.arange(int(SR * d)) / SR
    f = 300 + 1500 * np.abs(np.sin(2 * np.pi * 3.2 * t)) * np.exp(-t * 2)
    ph = 2 * np.pi * np.cumsum(f) / SR
    n = np.convolve(rng.normal(0, 1, t.size), np.ones(6) / 6, 'same')
    x = (0.22 * np.sign(np.sin(ph)) + 0.6 * n * (0.5 + 0.5 * np.sin(ph))) * np.exp(-t * 3.5)
    x[t > 0.42] *= 0.08
    return 0.55 * x
def ding():
    t = np.arange(int(SR * .5)) / SR
    return 0.22 * (np.sin(2 * np.pi * 1568 * t) + .6 * np.sin(2 * np.pi * 2093 * t)) * np.exp(-t * 9) * np.minimum(1, t / .004)
SFX = {'sting': sting, 'scratch': scratch, 'ding': ding}

parts = []
for i, (name, src, ss, dur, ovs, sfx, freeze) in enumerate(SEG):
    out = os.path.join(TMP, f'{i:02d}_{name}.mp4')
    n = int(SR * dur); fx = np.zeros(n)
    for kind, at in sfx:
        s = SFX[kind](); k = int(SR * at); fx[k:k + s.size] += s[:max(0, n - k)]
    fxw = os.path.join(TMP, f'{i:02d}_fx.wav'); wav(fxw, fx)
    inputs, fc = [], ''
    if src is None:
        inputs += ['-f', 'lavfi', '-t', str(dur), '-i', f'color=black:s=1080x1920:r=30', '-f', 'lavfi', '-t', str(dur), '-i', f'anullsrc=r={SR}:cl=stereo']
        fc = '[0:v]null[b0]'; vlast = 'b0'; aclip = '[1:a]'
    else:
        inputs += ['-ss', str(ss), '-t', str(dur), '-i', src]
        if freeze:
            clip = (f'[0:v]{VF},scale=1080:608,setsar=1,trim=end_frame=1,loop=loop=60:size=1:start=0,fps=30,hue=s=0.15,'
                    f'zoompan=z=\'1+0.0025*on\':d=1:s=1080x608:fps=30,trim=duration={dur}[clip]')
            aclip = None
        else:
            clip = f'[0:v]{VF},scale=1080:608:flags=lanczos,setsar=1,fps=30[clip]'
            aclip = '[0:a]'
        fc = clip + f';color=black:s=1080x1920:r=30:d={dur}[bg];[bg][clip]overlay=0:600:shortest=1[b0]'; vlast = 'b0'
    for j, (ov, at) in enumerate(ovs):
        inputs += ['-loop', '1', '-t', str(dur), '-i', os.path.join(H, 'ov', ov + '.png')]
        idx = inputs.count('-i') - 1
        fade = f',fade=in:st={at}:d=0.15:alpha=1' if at > 0 else ''
        fc += f';[{idx}:v]format=rgba{fade}[o{j}];[{vlast}][o{j}]overlay=0:0[v{j}]'; vlast = f'v{j}'
    fc += f';[{vlast}]format=yuv420p[v]'
    inputs += ['-i', fxw]; fxi = inputs.count('-i') - 1
    if aclip:
        fc += (f';{aclip}aresample={SR},aformat=channel_layouts=stereo,afade=t=in:d=0.03,afade=t=out:st={dur-0.05}:d=0.05[ca]'
               f';[{fxi}:a]aresample={SR}[fx];[ca][fx]amix=inputs=2:normalize=0:duration=first[a]')
    else:
        fc += f';[{fxi}:a]aresample={SR},aformat=channel_layouts=stereo[a]'
    run(['ffmpeg', '-y'] + inputs + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', str(dur),
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-ac', '2', out])
    parts.append(out)

lst = os.path.join(TMP, 'list.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
     '-r', '30', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-movflags', '+faststart', OUT])
print('done', OUT, round(sum(s[3] for s in SEG), 2), 's')
