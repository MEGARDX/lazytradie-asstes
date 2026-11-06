"""Vision film timeline (slow, warm cut): VO placement with real breathing room, the music edit that lands the
drop on V09, absolute word times and every scene key → timeline.json.   python3 timeline.py <words.json>"""
import json, sys
W = json.load(open(sys.argv[1]))                       # whisper words of the processed vo/*.wav
LINES = ['V01', 'V02', 'V03', 'V04', 'V05', 'V06', 'V07', 'V08', 'V09', 'V10', 'V11', 'V12', 'V13', 'V14']
# silence BEFORE each line (s). Bigger gaps where the picture changes scene.
GAP = {'V01': 1.4, 'V02': 1.4, 'V03': 1.2, 'V04': 1.0, 'V05': 1.6, 'V06': 1.2, 'V07': 1.8, 'V08': 1.0,
       'V09': None, 'V10': 1.4, 'V11': 1.4, 'V12': 1.4, 'V13': 1.8, 'V14': 2.0}
BEAT0, BEAT = 1.16, 1.0918                             # measured beat grid of assets/music.mp3
REP_B, REP_K = 14.26, 12                               # repeat the piano intro [B - 12 beats, B] once
REP_A = REP_B - REP_K * BEAT; X = REP_B - REP_A
DROP = 37.6 + X                                        # film time of the music drop
vo, words, prev = {}, {}, 0.0
for k in LINES:
    st = DROP + .45 if k == 'V09' else prev + GAP[k]
    vo[k] = round(st, 3); words[k] = [[w, round(st + a, 3), round(st + b, 3)] for w, a, b in W[k + '.wav']]
    prev = words[k][-1][2]
END = round(prev + 4.5, 2)
# outro: crossfade from the full section into the track's outro, on a beat, just before V13
jm = 37.6 + (vo['V13'] - .9 - DROP); n = round((jm - BEAT0) / BEAT); jm = BEAT0 + n * BEAT
JUMP = round(DROP + (jm - 37.6), 3)
MUSIC = [  # [film_start, music_start, music_end]
    [0.0, 0.0, REP_B], [REP_B, REP_A, REP_B], [REP_B + X, REP_B, jm], [JUMP, 108.6, 108.6 + (END - JUMP) + 1]]
def at(line, sub, which=1, end=False):
    w = [w for w in words[line] if sub.lower() in w[0].lower()][which - 1]; return w[2] if end else w[1]
K = {**{k.lower(): v for k, v in vo.items()}, **{'e' + k[1:]: words[k][-1][2] for k in LINES},
  'typeEnd': at('V01', 'tradies', end=True), 'gdp': at('V02', '%'), 'jobs': at('V02', 'million'),
  'biz': at('V03', 'half'), 'small': at('V03', 'small'), 'phone': at('V04', 'phone'),
  'pct27': at('V05', 'four'), 'unans': at('V05', 'unanswered'), 'pct3': at('V06', 'hundred'), 'msg': at('V06', 'message'),
  'goes': at('V06', 'goes'), 'priced': at('V07', 'priced'), 'big': at('V07', 'big'), 'missing': at('V08', 'missing'),
  'drop': round(DROP, 3), 'exists': at('V09', 'exists'), 'call': at('V10', 'call'), 'text': at('V10', 'text'),
  'web': at('V10', 'website'), 'booked': at('V10', 'booked'), 'tools': at('V11', 'tool'), 'p49': at('V12', '49'),
  'setup': at('V12', 'setup'), 'owned': at('V12', 'owned'), 'answers': at('V13', 'answers'), 'grows': at('V13', 'grows'),
  'built': at('V14', 'Built'), 'buildAus': at('V14', 'Australia'), 'jump': JUMP, 'end': END}
json.dump({'dur': END, 'vo': vo, 'k': {a: round(b, 3) for a, b in K.items()}, 'words': words, 'music': MUSIC},
          open('timeline.json', 'w'), indent=1)
for k in LINES: print(k, vo[k], '→', words[k][-1][2])
print('drop', round(DROP, 2), 'jump', JUMP, '(music', round(jm, 2), '→ 108.6)', 'end', END)
