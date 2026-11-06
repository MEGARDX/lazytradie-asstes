"""Vision film timeline: VO placement (beat-aware) + absolute word times + named sync keys → timeline.json"""
import json, sys
W = json.load(open(sys.argv[1]))           # whisper words of the processed vo/*.wav
PREF = {'V01': .45, 'V02': 3.2, 'V03': 11.2, 'V04': 15.85, 'V05': 18.4, 'V06': 24.3, 'V07': 29.75, 'V08': 33.85,
        'V09': 37.75, 'V10': 39.8, 'V11': 45.3, 'V12': 47.7, 'V13': 52.3, 'V14': 55.8}
vo, words, prev = {}, {}, 0
for k, p in PREF.items():
    ws = W[k + '.wav']; st = max(p, prev + .18); vo[k] = round(st, 3)
    words[k] = [[w, round(st + a, 3), round(st + b, 3)] for w, a, b in ws]; prev = words[k][-1][2]
    print(k, vo[k], '→', words[k][-1][2])
def at(line, sub, which=1, end=False):
    hits = [w for w in words[line] if sub.lower() in w[0].lower()]
    w = hits[which - 1]; return w[2] if end else w[1]
K = {**{k.lower(): v for k, v in vo.items()},
  'typeEnd': at('V01', 'tradies', end=True),
  'gdp': at('V02', '%'), 'gdpEnd': at('V02', 'economy', end=True), 'jobs': at('V02', 'million'), 'jobsEnd': at('V02', 'jobs', end=True),
  'biz': at('V03', 'half'), 'small': at('V03', 'small'),
  'phone': at('V04', 'phone'), 'v04': vo['V04'],
  'v05': vo['V05'], 'pct27': at('V05', 'four'), 'unans': at('V05', 'unanswered'),
  'v06': vo['V06'], 'pct3': at('V06', 'hundred'), 'msg': at('V06', 'message'), 'goes': at('V06', 'goes'),
  'v07': vo['V07'], 'priced': at('V07', 'priced'), 'big': at('V07', 'big'),
  'v08': vo['V08'], 'missing': at('V08', 'missing'),
  'drop': 37.6, 'v09': vo['V09'], 'exists': at('V09', 'exists'),
  'v10': vo['V10'], 'call': at('V10', 'call'), 'text': at('V10', 'text'), 'web': at('V10', 'website'), 'booked': at('V10', 'booked'),
  'v11': vo['V11'], 'tools': at('V11', 'tool'),
  'v12': vo['V12'], 'p49': at('V12', '49'), 'setup': at('V12', 'setup'), 'owned': at('V12', 'owned'),
  'v13': vo['V13'], 'answers': at('V13', 'answers'), 'grows': at('V13', 'grows'),
  'v14': vo['V14'], 'built': at('V14', 'Built'), 'buildAus': at('V14', 'Australia'),
}
BEATS = [1.14, 2.25, 3.34, 5.53, 8.8, 9.89, 12.07, 14.26, 17.53, 19.69, 21.87, 22.96, 26.24, 27.33, 28.42, 30.6, 31.7, 36.06, 37.6]
BEATS += [round(37.6 + .645 + 1.0905 * i, 2) for i in range(21)]
json.dump({'dur': 60.0, 'vo': vo, 'k': {a: round(b, 3) for a, b in K.items()}, 'words': words, 'beats': BEATS}, open('timeline.json', 'w'), indent=1)
print(json.dumps({a: round(b, 2) for a, b in K.items()}))
