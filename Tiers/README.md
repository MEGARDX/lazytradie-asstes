# LazyTradie Tutorial 1: Job Tiers (41 s)

The first tutorial in the series. Same design as the explainer: white theme, the real light-mode
dashboard and amber Copilot orb, real photos, a voiceover, professional SFX and **no background
music**.

- **Voiceover script:** [`voiceover-script.md`](voiceover-script.md) → `assets/vo/`
- **Photo prompts:** [`image-prompts.md`](image-prompts.md) → `assets/photos/`

---

## The finished film (`final/`)

Every export has **voice + sound effects only, no background music**, so your own music track can
go underneath. Both cuts share the same timeline, so the captions and any music edit work on both.

| File | What it is |
|---|---|
| `lazytradie-tiers-onboarding.mp4` | **Main cut, 16:9.** 41 s, 1920×1080, 30 fps, H.264 + AAC. Ends on "Let's set yours up." with a `Set up your tiers →` button, ready to hand off to the Knowledge Base tier setup. |
| `lazytradie-tiers-onboarding.webm` | The same cut as VP9 + Opus, for web `<video>` tags. |
| `lazytradie-tiers-brand.mp4` | Brand cut, 16:9: identical, but ends on the logo (no "Let's set yours up.", no button). For the help centre, website or socials. |
| `lazytradie-tiers.vtt` | Captions for the onboarding cut, one cue per sentence, timed to the voiceover. |
| `lazytradie-tiers-brand.vtt` | Captions for the brand cut. |
| `lazytradie-tiers-poster.png` | Poster frame for the `<video>` tag: the orb sorting three calls into the three tiers. |

The voiceover ran longer than the 30 s plan, so the film is 41 s and the edit follows the voice:
nothing is sped up or cut short.

**What's real in it.** The tier names, colours and pills (`T1 · Auto-book`, `T2 · Confirm`,
`T3 · Emergency`) are the dashboard's own. The bookings table and **Job tiers** donut at the end
are real light-mode dashboard screens rendered with the fictional demo account (Turner Electrical,
Melbourne). Nothing is a real customer. The Copilot is the real AI Orb (amber personality), driven
by the voiceover. The Tier 1 and Tier 2 job chips are the backend's own electrician presets, and
the Knowledge Base panels use the form's own trade-chip design.

**Sound.** Voice plus designed SFX, all synthesised, so there are no licensing strings. The film
reuses the explainer's SFX library and adds two new sounds, which are in `assets/sfx/`: a soft phone
ring for the hook and an urgent alert tone for Tier 3. The caller (TV_05) is treated as a
phone line in a room. Voice and effects sit at the explainer's levels: −14.6 LUFS (brand cut −14.8), true
peak under −1 dBTP. Every line was checked for intelligibility with speech recognition on the final mix.

**Adding your music.** The same rule as the explainer: keep the music about 9 dB below the voice,
dip it about 7 dB under speech, then bring the mix to −14 LUFS with true peak at −1 dBTP. The
Tier 3 section (21.4–31.9 s) has its own low drone, so pull the music right down or out there.

**Usage**
```html
<video poster="lazytradie-tiers-poster.png" autoplay muted playsinline controls>
  <source src="lazytradie-tiers-onboarding.webm" type="video/webm">
  <source src="lazytradie-tiers-onboarding.mp4" type="video/mp4">
  <track kind="captions" src="lazytradie-tiers.vtt" srclang="en" label="English" default>
</video>
```

---

## How tiers actually work (from the backend)

Every call the AI receptionist takes is sorted into one of three tiers. The rules come from the
agent prompt (`docs/shared-agent-draft.md`), the booking code (`services/bookingCreate.js`,
`services/availability.js`) and the Knowledge Base form (`auth-pages/knowledge-form.html`).

| Tier | Dashboard label | What goes in it | What the AI does |
|---|---|---|---|
| **Tier 1** | `T1 · Auto-book` (green) | Everyday jobs on the tradie's Tier 1 list. For electricians: power point install or replace, light fitting swap, smoke alarm replacement, ceiling fan install. | Checks the calendar, offers a free slot, confirms the customer's mobile and email, **books it straight in** and emails the customer a confirmation. |
| **Tier 2** | `T2 · Confirm` (amber) | Bigger jobs on the Tier 2 list (full switchboard upgrade, rewiring, EV charger), **anything likely $1,000+, and anything the AI isn't sure about**. | Takes the details and a preferred time, then **sends it to the tradie for review** ("In-Review"). The customer hears that someone will be in touch to lock it in. Tier 2 jobs can be scheduled over several days. |
| **Tier 3** | `T3 · Emergency` (red) | Anything dangerous or causing damage right now: sparking, burning smell, gas, flooding. No filtering by job type. | **Skips the normal booking flow.** Takes only the name, address and what's happening (the caller's number comes from the call), creates an emergency booking and **alerts the tradie straight away**. It gives the safety advice the tradie has switched on (call 000 for shock or fire, switch off at the main if safe) and promises a callback within the tradie's set window. |

The tradie decides what goes where in the Knowledge Base: Tier 1 and Tier 2 have preset example
jobs per trade plus custom ones, and the emergency protocol sets the callback and on-site targets.

---

## Beat sheet (as cut, 41.0 s)

The voice files are used as uploaded. `TV_08.mp3` holds script line TV_07 and `TV_09.mp3` holds
TV_08 (there is no `TV_07.mp3`); the edit maps them in that order.

| Time | Beat | VO (file) | Picture | SFX |
|---|---|---|---|---|
| 0.0–3.0 | **Hook** | TV_01 at 0.6 | Three incoming-call cards land, each with a caller photo and the job: "Light fitting swap", "Full switchboard upgrade", "Sparks from a power point". | phone ring, pops |
| 3.0–9.0 | **Sort** | TV_02 at 3.2 | The amber Copilot orb takes the calls. Three wires draw out to `T1 Auto-book`, `T2 Confirm first` and `T3 Emergency`, and the cards shuffle into their lanes. | shimmer, ticks, snap, whoosh |
| 8.4–14.7 | **Tier 1** | TV_03 at 8.6 | The "Tier 1 · Auto-book" title lands, then TP01 with real Tier 1 preset chips. A green `Confirmed` event drops into the calendar and a toast says "Confirmation emailed". | sub pulse, ticks, snap, success chime |
| 14.3–21.7 | **Tier 2** | TV_04 at 14.6 | The "Tier 2 · Confirm first" title, TP02 with Tier 2 chips and "Not sure? It asks you first". An `In-Review` job card fills in; on the TP07 inset the tradie taps **Approve** and the card flips to `Confirmed`. | ticks, pop, tap, ding |
| 21.4–31.9 | **Tier 3** (dark) | TV_05 caller at 22.0, TV_06 at 25.0 | The frame goes dark with a red glow. TP03 scorched outlet, and Emma's call card with a live transcript. The "Tier 3 · Emergency" title, then a checklist where the normal questions are struck out. An emergency alert lands ("callback within 15 min", "switch off at the main"), and the TP08 inset shows the tradie being alerted. A white circle wipe takes it back to light. | sub pulse, drone, phone buzz, alert tone, suck |
| 31.7–37.3 | **You choose** | TV_07 (`TV_08.mp3`) at 32.5 | Two Knowledge Base panels in light mode, with preset chips ticking on for Tier 1 and Tier 2. Then the real bookings table and **Job tiers** donut (T1 31 · T2 11 · T3 4), with tier rows highlighted. | ticks, whooshes |
| 36.9–41.0 | **End** | TV_08 (`TV_09.mp3`) at 37.4, onboarding cut only | Logo and tagline, plus a `Set up your tiers →` button in the onboarding cut. The brand cut ends on the logo. | end sting, logo hit |
