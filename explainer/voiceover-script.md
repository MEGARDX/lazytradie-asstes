# LazyTradie Explainer: Voiceover Script (60 s)

Copy each line into your TTS tool **exactly as written** and generate **one file per line**.
Save each file to `explainer/assets/vo/` with the filename shown. Timing, pauses and splits
are handled in the edit, so don't add pauses, music or effects to the files.

> **Check before generating:** these lines assume LazyTradie answers calls, quotes, books
> jobs into a calendar, chases invoices and quote follow-ups, builds quotes from a voice note,
> uses your own rates and branding, and connects to other tools. Strike or rewrite any line
> that isn't true for the product.

---

## Voice 1: Narrator (lines VO_01 to VO_07 and VO_09 to VO_14)

Modelled on the reference narrator: **deep, warm male voice** (the reference sits around
82 Hz, a low baritone), calm and confident, unhurried, smiling but not salesy. Think product
launch, not radio ad.

- **Accent:** Australian (recommended, since "tradie" is AU/NZ language). Use neutral
  English if you're targeting worldwide.
- **Pace:** natural, about 165 words per minute. Don't speed it up; the gaps come from the edit.
- **ElevenLabs-style settings:** Stability 50–60 %, Similarity 75 %, Style 0–15 %,
  Speed 1.0, Speaker boost on.
- **Takes:** generate 2–3 takes of VO_01, VO_02, VO_10 and VO_13, the lines that carry the video.

## Voice 2: Tradie on the phone (line VO_08 only)

Modelled on the reference's second voice (a user talking to the product).
**Real Aussie tradie**: casual, slightly gravelly, quick (the reference runs about 240 wpm),
talking to their phone between jobs. It **must be a different voice** from the narrator.
I'll add phone-mic EQ and light job-site room tone in the mix, so generate it clean.

## Pronunciation

`LazyTradie` = **LAY-zee TRAY-dee**. If the TTS says "tra-DIE" or runs it together oddly,
type `Lazy Tray-dee` in the TTS box only, and keep the filename the same.

---

## Lines

| File | Voice | Est. length | Plays at |
|---|---|---|---|
| `VO_01_hook.wav` | Narrator | 2.9 s | 0:00.8 |
| `VO_02_intro.wav` | Narrator | 1.5 s | 0:04.7 |
| `VO_03_calls.wav` | Narrator | 6.8 s (split in 3) | 0:07.7 |
| `VO_04_approve.wav` | Narrator | 3.8 s | 0:16.9 |
| `VO_05_proactive.wav` | Narrator | 2.2 s | 0:23.6 |
| `VO_06_chases.wav` | Narrator | 4.2 s | 0:26.4 |
| `VO_07_new_job.wav` | Narrator | 2.0 s | 0:31.6 |
| `VO_08_tradie_voice_note.wav` | **Tradie** | 4.6 s | 0:34.0 |
| `VO_09_builds.wav` | Narrator | 2.4 s | 0:39.0 |
| `VO_10_your_standards.wav` | Narrator | 3.4 s | 0:42.4 |
| `VO_11_pro_treatment.wav` | Narrator | 2.5 s | 0:46.6 |
| `VO_12_works_with.wav` | Narrator | 2.7 s | 0:50.2 |
| `VO_13_tagline.wav` | Narrator | 3.6 s | 0:54.0 |
| `VO_14_onboarding_cta.wav` | Narrator | 1.3 s | alt ending |

### VO_01_hook
```
Your admin can now take care of itself.
```

### VO_02_intro
```
Introducing LazyTradie.
```

### VO_03_calls
*(Generated as one sentence for natural flow. I'll split it at the two commas in the edit.)*
```
While you're on the tools, it answers every call, quotes the job, and books it straight into your calendar.
```

### VO_04_approve
```
One tap to approve, and your customer has it in seconds.
```

### VO_05_proactive
```
LazyTradie doesn't wait to be asked.
```

### VO_06_chases
```
It chases unpaid invoices, and follows up the quotes you forgot about.
```

### VO_07_new_job
```
Got a new job? Just tell it.
```

### VO_08_tradie_voice_note (Tradie voice)
```
Quote the Smith job. Two downlights, a new power point, and they want it done by Friday.
```

### VO_09_builds
```
LazyTradie builds it the way you would.
```

### VO_10_your_standards
*(Slow and deliberate, one beat between each sentence.)*
```
Your prices. Your terms. Your name on it.
```

### VO_11_pro_treatment
```
So every customer gets the pro treatment.
```

### VO_12_works_with
```
It works with the tools you already use.
```

### VO_13_tagline
```
Less admin. More time on the tools. With LazyTradie.
```

### VO_14_onboarding_cta (alternate ending)
*(Replaces the silent logo tail when the video plays inside onboarding and hands off to setup.)*
```
Let's get you set up.
```

---

**Totals:** 103 narrator words + 17 tradie words. That's the same density as the reference
(108 + 25 words in 64 s), scaled to 60 s with the same breathing room between lines.

**File format:** WAV, 48 kHz (44.1 kHz is fine), mono, 24-bit if your tool offers it.
MP3 at 192 kbps or higher works if WAV isn't available.
