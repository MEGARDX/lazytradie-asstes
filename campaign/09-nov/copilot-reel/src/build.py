#!/usr/bin/env python3
"""'Admin Copilot in LazyTradie' cinematic reel (after the Runway × Claude reference). python3 build.py → ../lazytradie-admin-copilot-reel-9x16.mp4
Needs: node shoot.js first (ov/*.png text overlays + ui/frame_*.png Copilot card animation).
Sources (owner's Veo clips + stills, 9:16): "9 Nov/gemini_generated_video_6c9ff9cc.mp4" (pile), "…_1301942c.mp4" (ask), "…_b64c5b2c.mp4" (stack);
img/tired.jpg = his photo B (watermark removed, upscaled) used for the tired beat (the clip's shot 2 was a different actor).
Clips muted; music bed = "9 Nov/leberch-ambient-cinematic-628167.mp3" from 0:48 so its lift lands on the Copilot card.
Cuts snap to the track's beat grid (0.836 s, anchored at 8.93 s). Every shot gets a slow push-in + warm grade + grain."""
import os, subprocess, wave, numpy as np

H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(H, '..', '..', '..', '..', '9 Nov'))
PILE, ASK, STACK = (os.path.join(SRC, f'gemini_generated_video_{k}.mp4') for k in ('6c9ff9cc', '1301942c', 'b64c5b2c'))
MUSIC = os.path.join(SRC, 'leberch-ambient-cinematic-628167.mp3'); MUSIC_IN = 48.0
TMP = os.path.join(H, 'tmp'); os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(H, '..', 'lazytradie-admin-copilot-reel-9x16.mp4')
FPS, SR = 30, 48000
DELOGO = 'delogo=x=568:y=1133:w=66:h=66'
GRADE = ('eq=contrast=1.05:saturation=1.05:gamma=0.97,colorbalance=rs=.04:gs=.01:bs=-.05:rm=.03:bm=-.03:rh=.02:bh=-.02,'
         'vignette=angle=PI/5,noise=alls=5:allf=t')
def push(dur, z1=1.07):  # slow centred push-in over the shot
    n = int(round(dur * FPS))
    return f"zoompan=z='1+{z1-1:.3f}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS}"

# (name, kind, src, start, dur, extra)
SEG = [
  ('pile',   'v', PILE,  0.20, 1.40, ''),
  ('tired',  'i', 'img/tired.jpg', 0, 1.68, ''),
  ('hands',  'v', PILE,  6.55, 2.51, ''),
  ('ask',    'v', ASK,   0.20, 3.34, ''),
  ('uibg',   'i', 'img/tired.jpg', 0, 6.69, 'boxblur=40:3,eq=brightness=-0.10:saturation=0.9,'),
  ('smile',  'v', ASK,   6.55, 3.35, ''),
  ('stack',  'v', STACK, 3.00, 3.34, ''),
  ('black',  'b', None,  0,    2.70, ''),
]
UI_AT = sum(s[4] for s in SEG[:4])           # 8.93
TEXT = [('title', 0.15, 2.75), ('quote', 6.30, 8.70), ('sub1', 16.10, 18.80), ('sub2', 19.40, 22.10), ('end', 22.31, 99)]
TICKS = [(UI_AT + t, k) for t, k in [(1.67, 't'), (2.51, 't'), (3.35, 't'), (4.18, 's'), (5.10, 't'), (5.45, 'c')]]

def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode: raise SystemExit(r.stderr.decode()[-2500:])

parts = []
for i, (name, kind, src, ss, dur, extra) in enumerate(SEG):
    out = os.path.join(TMP, f'{i:02d}_{name}.mp4')
    if kind == 'v':
        vf = f'{DELOGO},fps={FPS},scale=1080:1920:flags=lanczos,setsar=1,{push(dur)},{extra}{GRADE},format=yuv420p'
        run(['ffmpeg', '-y', '-ss', str(ss), '-t', str(dur), '-i', src, '-an', '-vf', vf, '-t', str(dur), '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', out])
    elif kind == 'i':
        vf = f'scale=1080:1920,setsar=1,{extra}{push(dur, 1.06)},{GRADE},format=yuv420p'
        run(['ffmpeg', '-y', '-loop', '1', '-framerate', str(FPS), '-t', str(dur), '-i', os.path.join(H, src), '-vf', vf, '-t', str(dur), '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', out])
    else:
        run(['ffmpeg', '-y', '-f', 'lavfi', '-t', str(dur), '-i', f'color=black:s=1080x1920:r={FPS}', '-vf', 'format=yuv420p', '-c:v', 'libx264', '-crf', '16', out])
    parts.append(out)

lst = os.path.join(TMP, 'list.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
base = os.path.join(TMP, 'base.mp4')
run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base])
TOTAL = round(sum(s[4] for s in SEG), 3)

# overlays: text PNGs with fades + the UI frame sequence
inputs = ['-i', base]; fc = '[0:v]null[v0]'; last = 'v0'
for j, (ov, a, b) in enumerate(TEXT):
    inputs += ['-loop', '1', '-t', str(TOTAL), '-i', os.path.join(H, 'ov', ov + '.png')]
    fo = f',fade=out:st={b-0.35}:d=0.35:alpha=1' if b < 90 else ''
    fc += f';[{j+1}:v]format=rgba,fade=in:st={a}:d=0.35:alpha=1{fo}[t{j}];[{last}][t{j}]overlay=0:0[v{j+1}]'; last = f'v{j+1}'
ui_idx = len(TEXT) + 1
inputs += ['-framerate', str(FPS), '-i', os.path.join(H, 'ui', 'frame_%04d.png')]
fc += f";[{ui_idx}:v]format=rgba,setpts=PTS+{UI_AT}/TB[ui];[{last}][ui]overlay=0:0:eof_action=pass[vu]"
fc += ';[vu]format=yuv420p[v]'

# audio: music bed + soft UI ticks
n = int(SR * TOTAL); fx = np.zeros(n); t = np.arange(int(SR * 0.4)) / SR
tick = 0.10 * np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 60)
swish = 0.06 * np.convolve(np.random.default_rng(3).normal(0, 1, t.size), np.ones(30) / 30, 'same') * np.sin(np.pi * np.minimum(1, t / 0.3))
chime = 0.12 * (np.sin(2 * np.pi * 1568 * t) + .6 * np.sin(2 * np.pi * 2093 * t)) * np.exp(-t * 8)
for at, k in TICKS:
    s = {'t': tick, 's': swish, 'c': chime}[k]; i0 = int(SR * at); fx[i0:i0 + s.size] += s[:max(0, n - i0)]
fxw = os.path.join(TMP, 'fx.wav')
with wave.open(fxw, 'wb') as w:
    st = np.stack([fx, fx], 1); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())
inputs += ['-ss', str(MUSIC_IN), '-t', str(TOTAL), '-i', MUSIC, '-i', fxw]
mi, fi = ui_idx + 1, ui_idx + 2
fc += (f';[{mi}:a]aresample={SR},aformat=channel_layouts=stereo,afade=t=in:d=0.4,afade=t=out:st={TOTAL-2.0}:d=2.0[mu]'
       f';[{fi}:a]aresample={SR}[fx];[mu][fx]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]')
run(['ffmpeg', '-y'] + inputs + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', str(TOTAL),
     '-c:v', 'libx264', '-crf', '20', '-maxrate', '14M', '-bufsize', '28M', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', str(FPS),
     '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-movflags', '+faststart', OUT])
print('done', OUT, TOTAL, 's; UI at', UI_AT)
