# LazyTradie Tutorial 1: Job Tiers (30 s)

The first tutorial in the series. Same design as the explainer: white theme, the real light-mode
dashboard and amber Copilot orb, real photos, a voiceover, professional SFX and **no background
music**.

- **Voiceover lines to generate:** [`voiceover-script.md`](voiceover-script.md) → `assets/vo/`
- **Photo prompts:** [`image-prompts.md`](image-prompts.md) → `assets/photos/`

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

## Beat sheet (30.0 s, locked to the VO once it arrives)

| Time | Beat | VO | Picture | SFX |
|---|---|---|---|---|
| 0.0–2.4 | **Hook** | TV_01 | Three incoming-call cards stack in, each with a caller photo and the job: "Light fitting swap", "Full switchboard upgrade", "Sparks from power point!" | phone ring, pops |
| 2.4–5.9 | **Sort** | TV_02 | The amber Copilot orb takes the calls. The cards fly into three lanes under the dashboard's own chips: `T1 · Auto-book`, `T2 · Confirm`, `T3 · Emergency`. | whooshes, three soft hits |
| 5.9–10.1 | **Tier 1** | TV_03 | TP01 + TP04. The calendar slot drops in as `Confirmed` (green) and a toast pops: "Confirmation emailed to customer". Real Tier 1 preset chips float in. | snap, success chime |
| 10.1–14.6 | **Tier 2** | TV_04 | TP02 + TP05. An `In-Review` card (amber) with the job details and preferred time. On TP07 the tradie taps **Approve** and the card flips to `Confirmed`. A small chip says "Not sure? It asks you first." | tick, tap, ding |
| 14.6–21.2 | **Tier 3** | TV_05 (caller) + TV_06 | The frame goes dark with a red tint. TP03 scorched outlet, TP06 caller with live waveform. An emergency card lands: "EMERGENCY · Sparking power point · Kew · callback within 15 min", with the safety advice line. TP08: the tradie's phone lights up with the alert. | alert tone, phone buzz, sub hit |
| 21.2–25.8 | **You choose** | TV_07 | Back to white. The Knowledge Base tier lists in light mode, with preset chips ticking on for Tier 1 and Tier 2. Then the real dashboard's **Job tiers** donut (T1 31 · T2 10 · T3 5). | ticks |
| 25.8–30.0 | **End** | TV_08 | Logo, tagline, and a `Set up your tiers →` button (onboarding cut). The brand cut ends on the logo. | end sting |

## Deliverables (same as the explainer)
16:9 and 9:16, each as an onboarding cut (ends on "Let's set yours up." + button) and a brand
cut (ends on the logo). Voice + SFX only, no music. Mastered at the explainer's levels.
Includes captions (`.vtt`) and posters.
