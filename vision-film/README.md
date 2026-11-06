# LazyTradie Vision Film: "Built for the people who build Australia" (1:27, 9:16)

A narrated motion-graphics vision film. **Tone: grow the nation.** Tradies are the backbone of the Australian
economy; missed calls quietly cost them jobs; the fix has been priced for big business; LazyTradie exists so
every tradie can answer every customer, and Australia grows with them.

- **Style reference:** the ElevenLabs Agents reel (`../Refrences/6 nov/SaveClip.App_AQNIqn…mp4`): one continuous
  shot, no hard cuts, dark with glows, each idea landing on a musical hit. Analysis in section 4.
- **Music:** `assets/music.mp3`, edited to the slow cut (see *Music edit* below), fading out over the last 4 s.
- **Voiceover:** [`voiceover-script.md`](voiceover-script.md) → `assets/vo/`
- **Every number** is sourced in [`DATA.md`](DATA.md) and shown on screen with a small source line.
- **Exports:** 9:16 1080×1920 (Reels/TikTok/Shorts) + 16:9 1920×1080 (website/YouTube), VTT captions.

**Look:** near-black → deep navy, **amber** glows (the real Copilot orb), touches of sky blue; a glowing
**dot-grid map of Australia** threads through the whole film. Liquid glass on cards and pills. JetBrains Mono for typed
lines and source tags, Inter Tight for everything else. Numbers **count up** and land on the beat.

## Music map (the original track, before the edit)
Pulse ≈ 55 BPM (a beat every 1.09 s). Quiet piano intro 0–18 s → swell at 18 s → build to **the drop at 37.6 s** →
full orchestra to 60 s. Hits used below: 1.14 · 2.25 · 3.34 · 5.53 · 8.8 · 9.89 · 12.07 · 14.26 · 17.53 · 19.69 ·
21.87 · 22.96 · 26.24 · 27.33 · 28.42 · 30.6 · 31.7 · 36.06 · **37.6** · then every 1.09 s (38.24, 39.33, 40.43 …) ·
**55.03** · 56.8 · 57.89.

---

## The finished film (`final/`)

| File | What it is |
|---|---|
| `lazytradie-vision-film-9x16.mp4` | **The film.** 1:27 (86.6 s), 1080×1920, 30 fps, H.264 (~9 Mbps) + AAC. Music + VO + SFX. |
| `lazytradie-vision-film.vtt` | Captions, one cue per line. |

**As built (slow, warm cut, 6 Nov):** jet black (#000, the grain is an overlay blend so it can't lift the blacks),
a warm amber dot map of Australia that tells the story (city glows, ringing phones, 27% of dots turning red, the amber
wave answering them west→east until the whole country glows, then morphing into the waving flag), the real LazyTradie
orb (`orb.js`, morning/amber personality) opening on the drop in a true-black Act 3, and liquid glass on every card,
pill, tag, the phone mockup and the price card. No pearls or gems. Every number carries its source on screen.
Pacing is documentary-slow: every line is spoken at natural speed with 1–2 s of air between lines, and each card
eases in over ~1.1 s and out over ~0.8 s. All picture and sound timings come from `src/timeline.json`.

**Music edit:** the piano intro is extended by repeating 12 beats (music 1.16–14.26 s, on the beat grid), so the
track's drop (37.6 s) lands at 50.7 s, right before "That's why LazyTradie exists". At 72.1 s, on a beat just before
V13, a 2 s crossfade takes it into the track's own outro (108.6 s), so the film ends on a resolving phrase.

**Sound:** the music edit, gently ducked under the VO (it breathes back up in the pauses); synthesised SFX tucked
under the music (keystrokes, counter ticks, distant Australian phone rings, missed-call blips, dust, price-tag thuds,
riser, sub boom + a warm chord bloom on the drop, booking chime, cloth flutter on the flag), all softer than the
first cut. −13.5 LUFS, −1.5 dBTP. Every VO line was checked for intelligibility on the final mix (Whisper).

**VO edit:** natural speed (no speed-up). Only silences longer than 0.75 s inside a line are shortened to 0.55 s
(`src/vo_prep.py`). No two lines overlap; the gaps between them are set in `src/timeline.py`.

**Rebuild:** `python3 src/vo_prep.py` → Whisper word times → `python3 src/timeline.py <words.json>` →
`node src/render.js <frames>` → `python3 src/audio.py <dir>` (music.wav, sfx.wav, vo.wav) → `src/mix.sh <dir> mix.wav` →
ffmpeg encode (crf 21, maxrate 9M).

---

## Storyboard (original 60 s plan; the slow cut keeps every scene and retimes it to the VO)

### Act 1 · The backbone (quiet intro, 0–18 s)
| # | Time | Picture | Lands on | VO |
|---|---|---|---|---|
| 1 | 0.0–5.5 | Black. A dot-grid **map of Australia** fades up, faint. Amber monospace types on: **"Australia was built by tradies."** | 1.14 · 2.25 · 3.34 | V01 |
| 2 | 5.5–9.9 | The map brightens around the cities. Big number counts up: **11.7%** *of Australia's GDP*, then **1.32 million** *jobs*. Source tag: *Master Builders Australia, ABS data, FY2024-25*. | 5.53 · 8.8 | V02 |
| 3 | 9.9–14.3 | **462,939** *construction businesses* counts up; a glass chip: **98.6% are small businesses**. Tiny ute icons scatter across the map. | 9.89 · 12.07 | V03 |
| 4 | 14.3–18.0 | Every dot on the map becomes a tiny phone, softly ringing. | 14.26 · 17.53 | V04 |

### Act 2 · The problem (swell + build, 18–37.6 s)
| # | Time | Picture | Lands on | VO |
|---|---|---|---|---|
| 5 | 18.0–22.9 | Swell. Some dots turn **red**. Glass cards cascade: *Missed call · SMS unread · Website form: no reply*. Number slams: **27%** *of calls to home-service businesses go unanswered*. Source: *Invoca, 2024*. | 19.69 · 21.87 | V05 |
| 6 | 22.9–27.3 | A voicemail icon drains: **fewer than 3%** *leave a message*. A job card ("Switchboard upgrade · $2,450") crumbles into dust and blows off-screen. | 22.96 · 26.24 | V06 |
| 7 | 27.3–31.7 | "The fix exists…" Price tags drop and stack like a bill, one per hit: **US$79 · US$99 · US$149 · US$150** /month. Source: *providers' pricing pages, 6 Nov 2026*. | 27.33 · 28.42 · 30.6 · 31.7 | V07 |
| 8 | 31.7–37.6 | The stack towers over a tiny ute icon. The red dots spread. Riser; everything inhales to black. | 36.06 | V08 |

### Act 3 · Why LazyTradie exists (THE DROP, 37.6–55 s)
| # | Time | Picture | Lands on | VO |
|---|---|---|---|---|
| 9 | **37.6**–40.4 | **Flash.** The amber orb bursts out of the black; the LazyTradie wordmark resolves: **"That's why LazyTradie exists."** | 37.6 · 38.24 · 39.33 | V09 |
| 10 | 40.4–45.9 | Glass chips lock in around the orb, one per beat, each ticking: **Calls ✓ · SMS ✓ · Website ✓ · Booked into your calendar ✓ · Admin by voice ✓** | 40.43 · 41.52 · 42.61 · 43.68 · 44.77 | V10 |
| 11 | 45.9–50.3 | A price card slams in: **A$49/month**, then stamps land beside it: **$0 setup · No lock-in · Australian owned** | 45.86 · 46.97 · 48.07 · 49.16 | V11 |
| 12 | 50.3–55.0 | Back to the map: a wave of **amber** sweeps across Australia from Perth to Sydney, turning every red dot to answered. Line: *Every call answered. Every tradie growing.* | 50.25 · 51.36 · 52.45 · 53.52 | V12 |

### Act 4 · The nation (55–60 s)
| # | Time | Picture | Lands on | VO |
|---|---|---|---|---|
| 13 | **55.03**–60 | The map's dots gather into a **vector Australian flag, waving smoothly** (a sine-wave cloth ripple across the stars and Union Jack). Below: the LazyTradie wordmark, **"Built for the people who build Australia."**, and `lazytradie.com.au`. Music fades out from 57 s. | 55.03 · 56.8 · 57.89 | V13 |

Sources line under the end card: *Master Builders Australia (ABS data, FY2024-25) · Invoca (2024) · provider pricing pages (6 Nov 2026)*.

---

## What I need
1. **13 voice lines** (`voiceover-script.md`), series narrator, warm and proud. This is a vision piece, not an ad read.
2. **Confirm "Australian owned"** is literally true (ownership, not just Melbourne-based). If unsure, I'll use "Built in Melbourne".
3. **Music licence:** Tunetank needs an active licence for commercial use; check whether your plan needs a caption credit.
4. Nothing else. The map, flag, orb, cards and numbers are all built in code.

## Sound
Music is the bed (first 60 s): under the VO at about −18 LUFS, full on the drop (37.6–40 s), ducking under V10–V13.
SFX on every beat-landing (soft glass ticks, a whoosh into the drop, a sub hit at 37.6 and 55.03, the faint phone
rings in scene 4). Final mix −14 LUFS, −1 dBTP.

---

## 4. Reference analysis (ElevenLabs Agents, 35.5 s, 720×1280)
One continuous shot: typed code-font line → the "o" becomes an orb → light bar ticker (API · VoIP · SDKs) → radar
dial → chat bubbles → "Lowest latency / Highest reliability" glow blob → agent dashboard with live transcript → task
card statuses → CRM ↔ Agent pills → code streak → logo end card. A calm narrator speaks 9 lines (~70 words) over
music; a new idea every 2–4 s, each landing on a hit.
