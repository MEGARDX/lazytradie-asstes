# LazyTradie Explainer: Production Plan & Asset List

A 60-second onboarding explainer with a white theme, a real voiceover, real photos and a
designed sound mix. It's modelled shot for shot on the ElevenLabs "ElevenAgents Architect"
launch video (`../snapgram.io_2kbkuhwskbf5.mp4`).

- **Voiceover lines to generate:** [`voiceover-script.md`](voiceover-script.md)
- **Drop finished assets into:** `assets/vo`, `assets/photos`, `assets/sfx`, `assets/music`,
  `assets/brand`, `assets/ui`

## The finished film (`final/`)

Every export has **voice + sound effects only, no background music**, so your own music track can
go underneath. All four videos share the same timeline, so the captions and any music edit work
on all of them.

| File | What it is |
|---|---|
| `lazytradie-explainer-onboarding.mp4` | **Main cut, 16:9.** 60 s, 1920×1080, 30 fps, H.264 + AAC. Ends on "Let's get you set up." with a `Get started →` button, ready to hand off to onboarding setup. |
| `lazytradie-explainer-onboarding.webm` | The same cut as VP9 + Opus, for web `<video>` tags. |
| `lazytradie-explainer-brand.mp4` | Brand cut, 16:9: identical, but ends on the logo (no VO_14, no button). For the website or socials. |
| `lazytradie-explainer-onboarding-9x16.mp4` | **Main cut, 9:16.** 1080×1920 vertical, for mobile onboarding. Every scene recomposed for portrait; same timing, sound and effects. |
| `lazytradie-explainer-onboarding-9x16.webm` | The 9:16 cut as VP9 + Opus. |
| `lazytradie-explainer-brand-9x16.mp4` | Brand cut, 9:16 (ends on the logo). For Reels, TikTok and Shorts. |
| `lazytradie-explainer.vtt` | Captions for the onboarding cuts (both shapes), timed to the voiceover. Onboarding videos usually autoplay muted, so turn these on. |
| `lazytradie-explainer-brand.vtt` | Captions for the brand cuts (no "Let's get you set up."). |
| `lazytradie-explainer-poster.png`, `…-poster-9x16.png` | Poster frames for the `<video>` tag (the logo reveal). |

**What's real in it.** The dashboard screens are the real LazyTradie dashboard in light mode with
the amber palette, rendered from the backend's own `dashboard.html` with a fictional demo
account (Turner Electrical, Melbourne). Nothing is a real customer. The Copilot is the real
AI Orb (`public/js/orb.js`, morning/amber personality) running in its recording mode, and it
reacts to the actual voiceover audio. The talk window, thinking line, quote cards and status
chips use the dashboard's own CSS. The receptionist is the real "Ruby" persona. Integrations
shown are only the live ones: Xero, ServiceM8, Fergus and Stripe.

**Sound.** Voice plus 22 designed SFX (`assets/sfx/`), all synthesised for this film, so there are
no licensing strings. The voice and effects sit at exactly the levels of the original mix
(−14.9 LUFS without music, −1 dBTP). The tradie's line (VO_08) is treated as a phone voice note.

**Adding your music.** To match the balance the film was mixed with: keep the music about 9 dB
below the voice, and dip it about 7 dB while someone is speaking (sidechain or keyframes), letting
it come back up between lines. Then bring the finished mix to −14 LUFS with true peak at −1 dBTP.
The original 90 BPM bed is still in `assets/music/` if you ever want it, but no export uses it.

**Usage in onboarding** (vertical file on phones, landscape everywhere else)
```html
<video poster="lazytradie-explainer-poster.png" autoplay muted playsinline controls>
  <source src="lazytradie-explainer-onboarding-9x16.mp4" type="video/mp4" media="(max-aspect-ratio: 3/4)">
  <source src="lazytradie-explainer-onboarding.mp4" type="video/mp4">
  <track kind="captions" src="lazytradie-explainer.vtt" srclang="en" label="English" default>
</video>
```

---

## 1. What the reference actually does

Analysed frame by frame (shot detection and 2 fps contact sheets), transcribed with word
timestamps, and measured with spectrograms and loudness metering.

### Structure (67.2 s, 20 cuts, average shot about 3 s)

| Time | Beat | Voiceover | Picture |
|---|---|---|---|
| 0.0–4.3 | Hook | "Your agents can now improve themselves." | Logomark pulse → typed words → 3 gradient tiles with tiny mono labels → one tile zooms to fill the frame |
| 4.3–7.5 | Brand | "Introducing ElevenAgents Architect." | Wordmark on a soft rounded-square grid; product name in the accent colour |
| 7.5–17.8 | Demo A | "Ask it anything… finds the root cause, recommends a fix, and builds it for you." | Prompt card types on a gradient → send click → UI panels float in → insight card → workflow icons pop in → step list |
| 17.8–19.0 | Approve | "Approve," | Reject / Approve buttons, cursor clicks, button fills with colour |
| 19.0–22.7 | Real people | "…pilot on live traffic before rolling out broadly." | **Real photo**: woman on phone + UI cards → floating photo collage |
| 22.7–25.7 | Dark interlude | "Architect doesn't wait to be asked." | Near-black, drifting particles, "Scanning conversations…" |
| 25.7–32.5 | Proactive | "It catches issues you've missed and proposes changes… pressure-tested against simulations." | Diff card → Proposals table → mosaic of passed tests |
| 32.5–35.4 | Transition | "Need a new agent?" | Gradient card → orb → "Ask Architect" pill |
| 35.4–45.0 | Demo B | "Just give Architect the context." + **second voice** dictating a request | Full-bleed gradient, words transcribe live, PDF/DOC icons drop onto the card |
| 45.0–48.5 | Result | "Architect builds it the way an expert would." | Real config UI (language, system prompt) |
| 48.5–50.6 | Statement | "To the standards you set." | Dark, kinetic type grey → white |
| 50.6–54.2 | Real customers | "So it's ready for real customers." | **3 real portraits**, one word each ("For / Real / Customers") → photo grid |
| 54.2–57.5 | Integrations | "Empower your team wherever they work." | "Connect Architect to — Claude / Cursor / ChatGPT…", hard cut every 0.67 s |
| 57.5–61.3 | Tagline | "Improve your agents and elevate your customer experiences with ElevenAgents Architect." | "Improve [orb] your agents" → "Elevate your customer experiences" |
| 61.3–67.2 | Logo | (voiceover ends at 63.7) | Logomark → wordmark, sting rings out until 65.5 |

### Look
- Warm off-white background, black type, one accent colour. Dark scenes appear only
  twice, as contrast "breaths".
- Blurred gradient "aura" images instead of illustrations. Clean product UI cards with soft
  shadows. Tiny monospace labels for detail.
- Real photos: candid, natural light, people on phones, mixed ages, never looking at the camera.
- Motion is calm: slow pushes, words revealed one at a time, cursor interactions. The only
  fast moment is the integration cut sequence near the end.

### Sound (measured)
| | Finding |
|---|---|
| Narrator | Deep, warm male voice (median pitch about 82 Hz), calm. **168 wpm while speaking, about 100 wpm overall**: 23 short lines with 0.6–1.8 s of space between them. Starts at 0.9 s. |
| Second voice | Casual user dictating to the product, fast (about 243 wpm), 7 s long, close-mic and natural. |
| Music | Minimal ambient electronic: sustained sub-bass, pads, soft pulses. Lifts at 0:19, thins out in the dark beats, resolves at the end with a tail. |
| Mix | Music sits only **about 6 dB under the voice** (−15.7 dB under speech vs −21.9 dB in gaps): a gentle dip, not a hard duck. |
| SFX | **Restrained.** Sub thumps on logo moments, soft UI clicks, ticks and pops, file-drop thuds, a resolving sting. Almost no big whooshes. Little energy above 6 kHz, so it sounds expensive, not bright. |
| Master | **−14.1 LUFS** integrated, 4.1 LU loudness range (consistent and compressed). |

---

## 2. LazyTradie beat sheet (60.0 s)

Every beat maps to a reference beat. Times are targets and get locked to the real voiceover
takes in the edit.

| Time | Beat | VO | Picture | SFX |
|---|---|---|---|---|
| 0:00.0–0:04.2 | **1 Hook** | VO_01 @ 0.8 | Off-white. LazyTradie mark pulses, then "Your admin" types in. Photo tiles PH01–PH03 float in with mono labels `NEW ENQUIRY · 7:42 AM`, `QUOTE SENT`, `INVOICE PAID`. At 3.8 one tile grows to fill the frame. | SFX_01 @ 0.0 · SFX_04 per word · SFX_15 @ 2.6 · SFX_02 @ 3.0 |
| 0:04.2–0:07.4 | **2 Brand** | VO_02 @ 4.7 | "LazyTradie" wordmark on the rounded-grid pattern; "for tradies" fades in beside it in the accent colour. | SFX_03 @ 4.2 |
| 0:07.4–0:16.6 | **3 Calls → quote → booking** | VO_03 @ 7.7 (split in 3) | PH02 plumber under sink, slow push in. Incoming call card `Sarah M. · Leaking tap` slides up and flips to "LazyTradie is answering…" with transcript bubbles. *"quotes the job"*: a quote card builds to `$264.00 inc. GST`. *"books it"*: calendar slot `Thu 8:00 AM · Leaking tap · Bondi` snaps in. | SFX_05 @ 7.5 · SFX_06 ×3 · SFX_04 per line · SFX_09 @ 15.4 |
| 0:16.6–0:19.2 | **4 Approve** | VO_04 @ 16.9 | Close-up of `Edit` / `Approve & send`. Tap on Approve at 17.6; the button fills with the accent colour. | SFX_07 @ 17.6 · SFX_08 @ 18.0 |
| 0:19.2–0:23.2 | **5 Customers** | (VO_04 carries over) | Music lifts. PH04 woman on phone in her kitchen, with the SMS card `Your quote from Dan's Plumbing · $264 · Accept` beside her. At 21.0 the frame pulls out into a floating collage (PH05–PH07 + UI cards). | SFX_10 @ 21.0 |
| 0:23.2–0:25.8 | **6 Dark interlude** | VO_05 @ 23.6 | Near-black, drifting particles, mono text `Checking unpaid invoices…` | SFX_11 @ 23.2 · SFX_12 @ 23.4 |
| 0:25.8–0:31.0 | **7 Follow-ups** | VO_06 @ 26.4 | Back to white. Follow-ups table: `INV-1042 · 14 days overdue → Reminder sent`, `Quote Q-311 · no reply 5 days → Follow-up sent`. At 29.6 a chip flips `Overdue` → `Paid`. | SFX_04 per row · SFX_08 @ 29.6 |
| 0:31.0–0:39.0 | **8 Voice note** | VO_07 @ 31.6 · **VO_08 @ 34.0** | PH08 tradie at ute → brand orb → `Hold to talk` pill. Full-bleed gradient + input card; the tradie's words transcribe live with the current word highlighted. Two job photos drop onto the card. | SFX_02 @ 30.4 · SFX_07 @ 33.2 · SFX_13 @ 33.6 · SFX_14 @ 36.4, 36.9 |
| 0:39.0–0:42.2 | **9 Built** | VO_09 @ 39.0 | Quote assembles: `2 × LED downlight supply & install`, `1 × double power point`, `Labour`, total, `Due Fri`. Chips fly in: `Your rate $95/hr`, `Call-out $80`, logo. | SFX_04 per line |
| 0:42.2–0:46.4 | **10 Statement** | VO_10 @ 42.4 | Dark. Kinetic type grey → white: "Your prices." "Your terms." "Your name on it." | music thins out |
| 0:46.4–0:50.0 | **11 Pro treatment** | VO_11 @ 46.6 | Portraits PH09, PH10, PH11 side by side, one word each: "Every" "Job" "Sorted". At 48.6 they slide up into a 3×3 grid (PH12–PH17). | SFX_10 @ 48.6 |
| 0:50.0–0:54.0 | **12 Integrations** | VO_12 @ 50.2 | Gradient cards hard-cut every 0.67 s: "Connect LazyTradie to — Xero / MYOB / QuickBooks / Google Calendar / Stripe". Real integrations only. | SFX_04 on each cut |
| 0:54.0–0:57.4 | **13 Tagline** | VO_13 @ 54.0 | "Less admin [orb] More time on the tools" → "Get your evenings back." over a dot field; PH18 at dusk optionally fades in behind. | — |
| 0:57.4–1:00.0 | **14 Logo** | VO_14 (onboarding cut only) | Mark pulse → wordmark. Onboarding cut adds a `Get started →` button. | SFX_01 + SFX_17 @ 57.4 |

---

## 3. Asset list

### A. Voiceover: 14 files
All lines, voice direction and settings are in [`voiceover-script.md`](voiceover-script.md).
That's 13 narrator lines plus 1 tradie line, and one alternate onboarding ending.

### B. Real photos: 18 images → `assets/photos/`

**Look rules (copied from the reference):** candid; subject looking at their phone or work,
not the camera; natural window or golden-hour light; shallow depth of field; warm neutral
colour; uncluttered backgrounds; **no visible logos or text**; mixed ages and genders;
Australian feel where possible (workwear, hi-vis, utes, brick and weatherboard homes).
**At least 3000 px on the long edge** so it can be cropped for 16:9 or 9:16.

| File | Shot | Used in | Search terms |
|---|---|---|---|
| `PH01_electrician_hands.jpg` | Electrician's hands at a switchboard or stripping wire, close crop | Hook tile | electrician hands wiring close up |
| `PH02_plumber_sink.jpg` | Plumber under a kitchen sink, both hands busy | Beat 3 hero | plumber under kitchen sink |
| `PH03_carpenter_timber.jpg` | Carpenter measuring or cutting timber outdoors, warm light | Hook tile | carpenter measuring timber, builder tape measure |
| `PH04_woman_phone_kitchen.jpg` | Woman (30–45) on a call in a bright kitchen | Beat 5 hero | woman on phone kitchen natural light |
| `PH05_homeowner_smiling_phone.jpg` | Homeowner smiling while reading their phone | Beat 5 collage | person smiling reading phone at home |
| `PH06_older_man_phone.jpg` | Man (60+) on a call in an armchair | Beat 5 collage | senior man phone call armchair |
| `PH07_couple_phone.jpg` | Couple looking at a phone together in a renovated living room | Beat 5 collage | couple looking at phone living room |
| `PH08_tradie_voice_note.jpg` | Tradie talking into their phone, leaning on a ute or van | Beat 8 opener | tradesman talking on phone van |
| `PH09_tradie_portrait.jpg` | Tradie in workwear, candid half-smile, on site (portrait) | Beat 11 "Every" | builder portrait candid smiling |
| `PH10_female_tradie.jpg` | Female electrician, painter or carpenter at work (portrait) | Beat 11 "Job" | female electrician, woman carpenter |
| `PH11_door_greeting.jpg` | Homeowner greeting a tradie at the front door (portrait) | Beat 11 "Sorted" | plumber greeting customer front door |
| `PH12_painter.jpg` | Painter rolling a wall | Beat 11 grid | painter roller wall |
| `PH13_tiler.jpg` | Tiler laying bathroom tiles | Beat 11 grid | tiler laying tiles |
| `PH14_landscaper.jpg` | Landscaper at work | Beat 11 grid | landscaper working garden |
| `PH15_roofer.jpg` | Roofer on a roof | Beat 11 grid | roofer working on roof |
| `PH16_apprentice.jpg` | Young apprentice with tool belt | Beat 11 grid | apprentice tool belt |
| `PH17_tradie_van_phone.jpg` | Tradie checking their phone in the van cab | Beat 11 grid | tradesman phone in van |
| `PH18_ute_dusk.jpg` | Ute or van on a suburban street at dusk | Beat 13 (optional) | work van suburban street sunset |

**Where to get them:** Pexels and Unsplash allow free commercial use, but don't present the
people as LazyTradie customers. Adobe Stock or iStock have model-released, Australia-specific
shots if the free ones look too American.

### C. Sound effects: 17 files → `assets/sfx/`
Each prompt works as-is in ElevenLabs Sound Effects (or as a search in Epidemic, Artlist or Freesound).
Keep them **soft and warm**. The reference never uses harsh or bright effects.

| File | Length | Used at | Prompt |
|---|---|---|---|
| `SFX_01_sub_pulse.wav` | 1.0 s | 0.0, 57.4 | Soft deep sub-bass pulse, single warm low thump with short decay, clean, no click, premium tech intro |
| `SFX_02_soft_riser.wav` | 1.2 s | 3.0, 30.4 | Soft airy reverse swell rising into a hit, filtered noise and tonal shimmer, subtle and gentle |
| `SFX_03_logo_hit.wav` | 2.5 s | 4.2 | Warm deep cinematic boom with soft airy shimmer tail, elegant brand logo reveal, not aggressive |
| `SFX_04_ui_tick.wav` | 0.15 s | about 25 uses: words, rows, cuts | Very soft minimal UI tick, tiny wooden click, clean, short |
| `SFX_05_phone_buzz.wav` | 1.5 s | 7.5 | Smartphone vibrating twice on a wooden workbench, close up, realistic |
| `SFX_06_ui_pop.wav` | 0.3 s | chat bubbles, cards | Soft bubbly UI pop, chat message appearing, gentle, modern app |
| `SFX_07_tap.wav` | 0.2 s | 17.6, 33.2 | Crisp soft touchscreen tap, button press, modern app, clean |
| `SFX_08_success.wav` | 0.8 s | 18.0, 29.6 | Subtle two-note success chime, message sent, warm and premium, not cartoonish |
| `SFX_09_snap.wav` | 0.3 s | 15.4 | Soft magnetic snap, UI element snapping into place |
| `SFX_10_air_whoosh.wav` | 0.5 s | 21.0, 48.6 | Very soft short air whoosh, subtle swipe transition, smooth, low volume |
| `SFX_11_dark_drone.wav` | 4.0 s | 23.2 | Low dark ambient room-tone drone with subtle movement, calm |
| `SFX_12_scan_shimmer.wav` | 3.0 s | 23.4 | Delicate granular digital shimmer, scanning data, soft sparkles, ambient |
| `SFX_13_mic_on.wav` | 0.4 s | 33.6 | Soft voice-assistant "start listening" blip, subtle |
| `SFX_14_photo_drop.wav` | 0.4 s | 36.4, 36.9 | Soft photo card dropping onto a table, light thud, close |
| `SFX_15_tape_measure.wav` | 0.6 s | 2.6 | Metal tape measure retracting fast and snapping shut |
| `SFX_16_drill_burst.wav` | 0.6 s | 1.9 (optional) | Short cordless drill burst, half a second, slightly distant on a job site |
| `SFX_17_end_sting.wav` | 3.0 s | 57.4 | Warm resolving synth chord swell with deep sub and soft shimmer tail, optimistic ending |

SFX_15 and SFX_16 are the "tradie" ear candy. The reference has nothing like them; they're
the one place this video can sound like LazyTradie rather than generic tech.

### D. Music: 1 track → `assets/music/MUS_01.wav`
Needs to be at least 65 s long. Download stems (bass / pads / pulse) if available, so I can
thin the track out in the dark beats.

Prompt for ElevenLabs Music, Suno or Udio:
```
Minimal premium tech product-launch music, 90 BPM, warm sustained sub bass, airy analog pads, soft plucked synth pulse, optimistic and calm, no vocals, no heavy drums, gentle lift at 0:19, sparse dark breakdown at 0:23, builds from 0:46, resolves cleanly at 0:57 with a 3 second ring-out, 65 seconds
```
For a stock library, search: *minimal tech ambient*, *warm corporate electronic*,
*product launch minimal*. 90 BPM matters because the 0.67 s integration cuts land on its beat.

### E. Brand & product (from you) → `assets/brand/`, `assets/ui/`
| Item | Notes |
|---|---|
| Logo | SVG: full wordmark and icon-only mark |
| Brand colours | Hex codes. If there aren't any, I'll propose off-white `#F7F6F3`, ink `#111111`, a hi-vis orange accent, and steel-blue / sand gradients |
| Font | If you have one; otherwise Inter + JetBrains Mono (free, matches the reference's clean grotesk + mono labels) |
| App screenshots | Incoming call / transcript · quote with line items · calendar booking · approve & send · what the customer receives · invoices / follow-ups list · voice-note input · settings (rates, branding). I rebuild these as clean vector cards like the reference does; the screenshots keep them accurate. If a screen doesn't exist yet, say so and I'll design it. |
| Integrations | The real list, for beat 12 |

### F. Made in code (nothing to download)
Gradient aura backgrounds and the orb (in brand colours), rounded-square grid pattern,
particle and dot fields, all UI cards, kinetic type, captions file (`.vtt`) for muted autoplay
in onboarding.

---

## 4. Output specs
- **Master:** 1920×1080, 30 fps, H.264 MP4 + WebM, poster frame PNG.
- **Mix:** VO-first; music about 6 dB under the voice; −14 LUFS integrated, −1 dBTP true peak.
- **Versions:** *Brand* (silent logo ending) and *Onboarding* (VO_14 + `Get started →`).
- A 9:16 vertical cut is possible if onboarding runs in a mobile app; the photo spec above
  already covers it.
