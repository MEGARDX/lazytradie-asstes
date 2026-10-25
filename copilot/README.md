# LazyTradie Admin Copilot (1 min 43 s)

A premium film showing the Admin Copilot running a tradie's day **by voice**. It's modelled on the
first minute of the ElevenLabs "Introducing Eleven v4" film. The picture switches between **white
and navy** ten times, using the real amber Copilot orb and the dashboard's own Copilot cards.

**There are no photos or generated video in it.** Everything on screen is real product UI and
motion graphics. The only external resources were the 20 voice lines (`assests/`,
[`voiceover-script.md`](voiceover-script.md)).

---

## The finished film (`final/`)

| File | What it is |
|---|---|
| `lazytradie-admin-copilot.mp4` | **The film.** 1:43, 1920×1080, 30 fps, H.264 + AAC. Voice + SFX, **no music**. |
| `lazytradie-admin-copilot.webm` | The same film as VP9 + Opus, for web `<video>` tags. |
| `lazytradie-admin-copilot.vtt` | Captions, one cue per sentence, with the speaker on each (`Narrator`, `Jack`, `Copilot`). |
| `lazytradie-admin-copilot-poster.png` | Poster frame: Schedule, with the orb, the transcript and today's jobs. |

The voice lines ran to 82 s of pure speech (the Copilot's real voice is unhurried), so the film is
1:43 rather than 60 s. Nothing is sped up. The only edit to the voices is tightening the Copilot's
longest thinking pauses to a natural length.

**As cut:**

| Time | Theme · wipe in | Scene |
|---|---|---|
| 0:00 | White | Intro: "Everything you're about to see gets done by voice…" blurs in word by word, ending on a `Copilot` chip. |
| 0:08 | White → **navy** (burst) | The real orb pops in, becomes five waveform bars, then three thinking dots, then bursts. Navy floods out and the two speakers form: **Jack** (a particle sphere that ripples with his voice) and the **Copilot** orb. "Good morning! What can I sort out for you?" |
| 0:13 | Navy | **01 Schedule:** "What's on today?" Today's four jobs build in and the first one is ringed. |
| 0:21 | **White** · pixel mosaic | **02 Find jobs:** the query types into search and Sarah's job card resolves (`T2 · In review`). |
| 0:32 | **Navy** · circle out of the orb | **03 Manage jobs:** "Approve it, and move it to Friday at two." The pill flips to `Confirmed` and her booking lifts off Thursday 9 AM and lands on Friday 2 PM. |
| 0:41 | **White** · rising bars | **04 Book a job:** the booking card fills in as Jack talks. The Copilot asks to confirm, "Yep.", and it turns green and drops into Wednesday's calendar. |
| 0:58 | **Navy** · dot matrix | **05 Notes & reminders:** "bring the long ladder" types onto Mike's job and saves. |
| 1:06 | **White** · iris into the orb | **06 Quotes:** the real quote card builds to $2,450, then the confirm card. The cursor taps **Confirm** and the quote is sent. |
| 1:19 | **Navy** · sliding pills | **07 Invoices:** the invoice builds to $380 and is confirmed and sent, with a card pay link (Stripe). |
| 1:29 | **White** · diagonal mosaic | Recap: "Schedule." "Jobs." "Quotes & invoices." "Sorted." The feature icons orbit and get pulled into the full stop. |
| 1:36 | **Navy** · out of the full stop | Sign-off: the orb takes centre stage and Jack's sphere orbits it. "Afternoon, mate. What's next on the list?" |
| 1:40 | **White** · circle out of the orb | End card: LazyTradie wordmark, `Admin Copilot`, "Just ask." |

**Sound.** Three voice chains:
- **Narrator:** the explainer's exact chain.
- **Copilot:** clean and close, since it's the product's own voice.
- **Jack:** a light phone-mic feel.

On top of that, 133 designed SFX cues, every one on a picture event. The mic "blip" opens and closes
around each of Jack's lines, like the real Talk mode. Mastered with the series' limiter: −14.8 LUFS,
true peak −1.2 dBTP. Every line was checked for intelligibility with speech recognition on the
final mix.

**What's real:**
- Every request and reply is something the Copilot actually does today, per the backend's tool
  registry and voice rules.
- The cards are the dashboard's own Copilot components in its light and dark tokens, on the
  fictional demo account (Turner Electrical, Melbourne).
- Payment reminders aren't live yet, so "Notes & reminders" shows a job note, which is.

**Adding your music.** Same rule as the other films: keep it about 9 dB under the voice, dip it
about 7 dB under speech, then master to −14 LUFS with true peak at −1 dBTP.

---

## What the reference does (first 60 s of a 156 s vertical film)

| Time | What you see | What you hear |
|---|---|---|
| 0.0–8.5 | Warm off-white. Three small centred lines blur in one at a time, ending on an inline `v4` chip. | Narrator: "Everything you're about to hear was generated from the prompts shown, with no edits or modifications. Just Eleven v4…" |
| 8.5–12.5 | The text blurs out. A gradient orb pops in, breathes, shrinks to a dot, stretches into five rounded waveform bars, then collapses into three "thinking" dots. | "…a speech model that doesn't just speak, it performs." |
| 12.5–13.5 | The dots burst into a soft colour bloom and drifting particles. The particles gather into two stippled faces. | |
| 13.5–51.0 | **The performance.** Two particle faces (one green, one red) light up as they speak. Underneath, the script plays as a live karaoke line: the spoken word in colour, audio tags like `[whispering nervously]` in grey. | A short film-set scene between a director and an actor, with whispers, crying, laughter and a British accent. |
| 51.0–60.0 | The faces dissolve into the orb. Orbs slide inside white pill tracks like sliders, then a pixel-mosaic wipe, the word "Intent." with a colour-shifting full stop, and two orbs orbiting a ring. | Narrator: "But voice carries more than just sound. It carries tone, texture, intent…" |

**Why it feels AAA:**
- One continuous canvas, no hard cuts. Every scene grows out of the last shape: orb → bars → dots → particles → faces → orb.
- Generous empty space and small type.
- The words are the star: you read what you hear, as you hear it.
- A soft bed of sound under everything (−14.2 LUFS).

---

## The plan (as written before the voice arrived)

### Beat sheet (planned at ≈60 s; see "As cut" above for the real timing)

Three voices:
- **Narrator:** the explainer's voice.
- **Jack:** the tradie, giving commands.
- **Copilot:** Deepgram's **Sharon** (`flux-sharon-en`), the real product voice.

The Copilot's lines follow its real speaking rules from the backend:
- It opens with a 2–5 word lead-in ending in "…".
- It answers in one or two short sentences.
- It turns a booking into a short confirm question.
- It never sends by voice: it says "Tap confirm to send."

| Time | Theme | Feature | Audio | Picture |
|---|---|---|---|---|
| 0.0–7.5 | White | Intro | N_01 | Three lines blur in, centred and small, ending on a `Copilot` chip with a tiny amber orb. |
| 7.5–11.5 | White → **Navy** | The orb wakes | CV_00 (real recorded greeting) | The real orb pops in and breathes, then stretches into five amber waveform bars and collapses into three thinking dots. The dots burst, and navy floods out from the burst. Two "speakers" form: **You** (a particle sphere that ripples with Jack's voice) and the **Copilot** orb. |
| 11.5–16.5 | Navy | **01 · Schedule** | TR_01 → CV_01 | A live transcript line types Jack's words, then the Copilot's in amber. Today's four jobs slide in as a timeline. |
| 16.5–22.0 | **White** (pixel-mosaic wipe) | **02 · Find jobs** | TR_02 → CV_02 | The search query types itself, and Sarah's job card resolves out of the pixels with an amber `In review` pill. |
| 22.0–26.5 | **Navy** (the orb expands into a circle wipe) | **03 · Manage jobs** | TR_03 → CV_03 | The pill flips to `Confirmed`. Her calendar block lifts off Thursday 9 AM and drops onto Friday 2 PM. |
| 26.5–33.0 | **White** (bars sweep) | **04 · Book a job** | TR_04 → CV_04 → TR_05 → CV_05 | The booking confirm card fills in field by field (Mike Chen · Two downlights · Fitzroy · Tomorrow 10 AM). On "Yep" it snaps into the calendar with a success flash. |
| 33.0–37.0 | **Navy** | **05 · Notes & reminders** | TR_06 → CV_06 | A note chip ("Bring the long ladder") drops onto Mike's job. |
| 37.0–43.5 | **White** | **06 · Quotes** | TR_07 → CV_07 | The real quote card builds its lines and a $2,450 total; a cursor taps **Confirm** and it reads `Sent`. |
| 43.5–49.0 | **Navy** | **07 · Invoices** | TR_08 → CV_08 | The invoice card builds for Liam, $380. **Confirm** is tapped and a Stripe pay link chip appears. |
| 49.0–55.0 | **White** | Recap | N_02 | Big kinetic words, one per beat: "Schedule." "Jobs." "Quotes." "Invoices." then "Sorted." with an amber full stop that colour-shifts, as in "Intent.". |
| 55.0–60.0 | Navy → white | End | CV_09 (real recorded greeting) | The two speakers orbit a ring and merge into the orb. End card: LazyTradie wordmark, `Admin Copilot`, "Just ask." |

A small mono label sits top-left in every feature scene (`01 · SCHEDULE` … `07 · INVOICES`), so
the features read as a list even with the sound off.

**What's real:**
- **Abilities:** every request and reply is something the Copilot actually does today, per the
  backend's tool registry (`services/copilot/registry.js`) and its voice rules.
- **Screens:** the cards are the dashboard's own Copilot cards on the fictional demo account
  (Turner Electrical, Melbourne).
- **The two greetings:** recorded product clips from `public/voice/greetings/`
  ("Morning! What can I sort out for you?", "Afternoon, mate. What's next on the list?").

**Reminders:** the Copilot can't send payment reminders yet; the backend marks them "coming soon".
"Notes & reminders" therefore shows a job note ("bring the long ladder"), which is live, and the
film never claims it chases payments.

---

### Resources

| What | Where it comes from | Status |
|---|---|---|
| Narrator lines N_01, N_02 | ElevenLabs, the explainer's narrator voice | **You make** |
| Jack's lines TR_01–TR_08 | ElevenLabs, a relaxed Australian male (see the voice brief) | **You make** |
| Copilot lines CV_01–CV_08 | Deepgram TTS, **Sharon** (`flux-sharon-en`), the real product voice | **You make** |
| Copilot greetings CV_00, CV_09 | The recorded product clips in the backend | Have them |
| The orb, the dashboard cards, the wordmark | Real product code and brand files | Have them |
| SFX | Designed for this film (the explainer library plus new UI sounds) | I make |

Deliverable: 16:9, 1920×1080, 30 fps. Voice and SFX only, **no music**, so your own track can go
under it, as with the other films.
