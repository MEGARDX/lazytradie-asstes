# LazyTradie AI Receptionist Reel: Plan & Asset List (≈44 s)

A motion-graphics launch reel for the **AI Receptionist**, modelled beat for beat on the ElevenLabs
**"Introducing Vocals on Eleven Music"** reel
(`../SaveClip.App_AQNHIk458UOcVM-8WIgdltAADdKlL_09EDfgsWGiODGkIJNO0Rr-T7Zjds_sb0rc-OluXBtQV3Vol_l1DHnKknEf82sMHVP4TQGfoaM.mp4`).

- **Voiceover lines:** [`voiceover-script.md`](voiceover-script.md) → `assets/vo/`
- **Photos:** the six trade photos below → `assets/photos/`
- Everything else (orb, UI, cards, type, transitions, SFX) I build in code from the real product.

**Exports:** `1:1` 1080×1080 (main, same shape as the reference, for the IG/FB feed) and
`9:16` 1080×1920 (Reels, TikTok, Stories), recomposed per scene. 30 fps, H.264 + AAC, plus VTT captions.

---

## 1. What the reference does (42.0 s, 720×720, 30 fps)

Frame-by-frame at 2 fps, word-timed transcript, loudness measured.

| Time | Picture | Voiceover |
|---|---|---|
| 0.0–3.3 | Black. "Vocals" blurs in letter by letter, two thin bars slide in to bracket it, then the bars collapse into the Eleven logomark, which twists and shrinks away. | "Introducing Vocals on Eleven Music." |
| 3.3–5.3 | A gradient pill grows into an `Upload samples` button. Three file thumbnails with filenames fly in diagonally and stack under it. | "Create a vocal from your existing tracks." |
| 5.3–7.0 | The button morphs into a large frosted teal orb. A warped grid of glowing teal lines bends around it like a gravity well, then the orb shrinks. | "Then generate new songs with studio-level consistency" |
| 7.0–11.5 | The orb becomes the avatar in a voice chip, `Aurora · Ethereal pop soprano`. The chip slides off and a dot draws a line that **branches into three glowing track bars**, which settle into a dim track list. | "…and that same voice anytime." |
| 11.7–17.0 | A ghost `Record` button lights up blue (`Record a sample`), then expands into a dark recorder with a red waveform and playhead, drifting slowly towards camera. | "Prefer to start afresh? Upload a single voice recording." |
| 17.0–22.3 | The recorder drops onto a teal orb, then cuts to a **full-frame grainy teal gradient** with one frosted player card (`Chasing Shadows · Aurora · 3:50`). The gradient slowly drifts. | "And turn it into an original track in your own voice." |
| 22.3–27.0 | A real app sidebar slides in (`Studio, Tools, Styles, Vocals`). `Vocals` is selected and the camera pushes into the **Singing Vocals library** grid, then it dims away. | "Or skip setup entirely and choose a voice straight from our vocal library." |
| 27.0–29.0 | "Styles" blurs in, holds and blurs out. | "We're also bringing styles to Music V2," |
| 29.0–31.2 | A slow 3D carousel of square cover art orbiting in depth, on a faint teal ellipse. | "making it easier than ever to create tracks…" |
| 31.2–34.6 | **Photo montage:** two candid flash photos side by side, swapping every ~0.4 s (piano, drums, party, orchestra, crowd, DJ). A white curved wipe ends it. | "…with a consistent sound, mood and identity." |
| 34.6–42.0 | The giant logomark slams in, shrinks into a rounded-square frame. The frame holds the `Eleven Music` wordmark and the URL types on with a cursor. | "Vocals and styles are available today on Eleven Music. Make your next track unmistakably yours." |

**Look:** pure black, one accent colour (teal), white neo-grotesk type, soft glows, frosted glass
and slow camera drift. Every scene morphs out of the one before: nothing hard-cuts until the montage.
**Sound:** one calm female narrator over a soft music bed, mixed loud (−14.1 LUFS, LRA 3.1).
12 lines, ~92 words in 40 s.

---

## 2. The LazyTradie version: beat sheet

Same structure, same morph-from-the-last-scene logic. Teal becomes **amber**, black becomes the
dashboard's **deep navy** (`#060d18`), and the orb is the **real amber Copilot orb** (`public/js/orb.js`).
Liquid glass on the chip, the booking card, the buttons and the end-card frame.

| Time | Picture | Line |
|---|---|---|
| 0.0–3.3 | "Receptionist" blurs in, bracketed by two amber bars. The bars collapse into the LazyTradie gear-and-spanner icon, which twists away. | R_01 |
| 3.3–5.6 | A pill grows into `Set up your AI receptionist`. Three real setup cards fly in and stack: `Your services`, `Service area`, `Business hours` (the wizard and Knowledge Base fields). | R_02 |
| 5.6–7.6 | The button morphs into the amber orb. A warped amber grid bends around it. | R_03 |
| 7.6–11.5 | The orb becomes the avatar in a glass chip, `Turner Electrical · AI Receptionist`. A dot draws a line that branches into three glowing bars: `📞 Call`, `💬 SMS`, `🌐 Web enquiry`. | R_04 |
| 11.7–17.0 | A ghost button lights up amber: `Incoming call`. It expands into a dark live-call card: caller waveform, timer, and the free slots lighting up one by one (`Mon 9:00 ✓`). | R_05, R_06 |
| 17.0–22.3 | The card drops onto the orb, then a full-frame **grainy amber-to-navy gradient**, drifting, with one liquid-glass card: `✓ New job booked · Sarah Mitchell · Power point install · Mon 9:00 AM · T1`. | R_07 |
| 22.3–27.0 | The real dashboard sidebar slides in (`Dashboard, Jobs, Knowledge Base, Integrate Tools, AI Agent for Website`). `Jobs` is selected and the camera pushes into the real Jobs table. | R_08 |
| 27.0–29.0 | "Job Tiers" blurs in and out. | R_09 |
| 29.0–31.2 | A slow 3D carousel of job cards orbiting in depth, each with a tradie photo and its tier pill: green `T1`, amber `T2`, red `T3`. | R_10 (first half) |
| 31.2–34.6 | **Photo montage:** two trade photos side by side, swapping every ~0.4 s. An amber curved wipe ends it. | R_10 (second half) |
| 34.6–44.0 | The giant icon slams in, shrinks into a glass rounded-square frame holding the LazyTradie wordmark. `lazytradie.com.au` types on with a cursor. | R_11, R_12 |

**Sound:** the series narrator plus designed SFX (whooshes, glass ticks, the call ring, a booking
chime), mixed to −14 LUFS, true peak −1 dBTP. The reference has a music bed. Per the series rule,
the export is **voice + SFX only** with room left for your track: keep music ~9 dB under the voice
and dip it ~7 dB under speech.

---

## 3. Photos

### Montage: 12 photos, paired left/right

| Pair | Left | Right |
|---|---|---|
| 1 | `electrician` (new) | `29 oct/non edited/1 A.jpg` (her on the ladder) |
| 2 | `plumber` (new) | `29 oct/non edited/2 A.jpg` (the guy in the ute) |
| 3 | `carpenter` (new) | `26 oct/alternate of paint pour.jpg` (the paint roller) |
| 4 | `hvac` (new) | `29 oct/non edited/4 B.jpg` (her fist pump) |
| 5 | `landscaper` (new) | `26 oct/ute tray hammock , alternate of Pool float.jpg` |
| 6 | `roofer` (new) | `31 oct` weekend tailgate shot |

The same photos feed the job cards in the 3D carousel. Only the **six new trade photos** need
generating. The prompts are below, all 4:5. Save them to `assets/photos/` as `electrician`,
`plumber`, `carpenter`, `hvac`, `landscaper`, `roofer`.

**Style block** (already in each prompt):
> Shot on 35mm film, hard direct sun, crisp shadows, saturated colour, fine grain. Palette strictly
> deep navy (#0D1B2A), marigold amber (#F5A623), warm off-white and a touch of sky blue. Bold, playful,
> premium lifestyle advertising for an Australian trades brand. Models are young, radiant, styled
> like a fashion shoot. No food or drinks. No text except "LazyTradie" exactly as written.

**plumber**
```
A handsome 25-year-old male model plumber, tousled sun-bleached hair, light stubble, crouched low in front of an open under-sink cabinet in a bright modern kitchen with deep navy cabinetry. He wears a fitted navy work shirt with the sleeves rolled to the elbows and a small amber "LazyTradie" logo on the chest. One hand grips a glossy marigold-amber pipe wrench on the chrome trap under the sink, and he glances back over his shoulder at the camera with a confident half-smile. An open amber toolbox sits beside him on the warm off-white tiled floor. Hard sun streams through a side window, throwing crisp graphic shadows across the cabinets. Framed from a low side angle, full body, with clean space above him. 4:5.

Shot on 35mm film, hard direct sun, crisp shadows, saturated colour, fine grain. Palette strictly deep navy (#0D1B2A), marigold amber (#F5A623), warm off-white and a touch of sky blue. Bold, playful, premium lifestyle advertising for an Australian trades brand. Models are young, radiant, styled like a fashion shoot. No food or drinks. No text except "LazyTradie" exactly as written.
```

**electrician**
```
A striking 24-year-old female model electrician with a sleek dark ponytail and gold hoop earrings stands at an open residential switchboard mounted on a deep navy painted brick wall. She wears clear safety glasses pushed up slightly, marigold-amber insulated electrical gloves, and a fitted white work tee under an open amber hi-vis vest with a small "LazyTradie" patch. One gloved hand rests on the switchboard door while she checks the breakers with calm, focused confidence, a slight knowing smile. A digital multimeter hangs from her tool belt. Hard side sun throws a crisp diagonal shadow of her and the open panel door across the navy wall. Framed from the waist up, three-quarter angle, with negative space on one side for a headline. 4:5.

Shot on 35mm film, hard direct sun, crisp shadows, saturated colour, fine grain. Palette strictly deep navy (#0D1B2A), marigold amber (#F5A623), warm off-white and a touch of sky blue. Bold, playful, premium lifestyle advertising for an Australian trades brand. Models are young, radiant, styled like a fashion shoot. No food or drinks. No text except "LazyTradie" exactly as written.
```

**carpenter**
```
A rugged, handsome 26-year-old male model carpenter with wavy hair and a carpenter's pencil tucked behind one ear, leaning over a length of pale fresh-cut timber laid across two navy-painted sawhorses. He pulls a marigold-amber tape measure along the board, marking it with a small tick, eyes on the cut, a relaxed satisfied smile. He wears a crisp white tee, navy work pants and a tan leather tool belt with "LazyTradie" stamped on the pouch. Fine sawdust drifts and glows in the sun, with curls of wood shavings on the ground. The backdrop is a clean warm off-white rendered wall. Hard late-afternoon sun from the side, crisp shadows of the sawhorses. Framed from the thighs up. 4:5.

Shot on 35mm film, hard direct sun, crisp shadows, saturated colour, fine grain. Palette strictly deep navy (#0D1B2A), marigold amber (#F5A623), warm off-white and a touch of sky blue. Bold, playful, premium lifestyle advertising for an Australian trades brand. Models are young, radiant, styled like a fashion shoot. No food or drinks. No text except "LazyTradie" exactly as written.
```

**hvac**
```
A fit 25-year-old male model HVAC technician with a short fade and light stubble kneels beside a clean white outdoor air-conditioning unit mounted against a deep navy weatherboard wall. He tightens a fitting on the copper refrigerant lines with a marigold-amber spanner, gauges hanging from the unit, and looks up at the camera with an easy, confident grin. He wears a navy work polo with a small amber "LazyTradie" logo, navy work shorts and dusty boots. A sky-blue sky shows at the top edge of the frame. Hard midday sun throws crisp shadows of the unit's fan grille across the wall. Shot from a slightly low angle, full body, graphic and clean. 4:5.

Shot on 35mm film, hard direct sun, crisp shadows, saturated colour, fine grain. Palette strictly deep navy (#0D1B2A), marigold amber (#F5A623), warm off-white and a touch of sky blue. Bold, playful, premium lifestyle advertising for an Australian trades brand. Models are young, radiant, styled like a fashion shoot. No food or drinks. No text except "LazyTradie" exactly as written.
```

**landscaper**
```
A stunning 23-year-old female model landscaper with sun-kissed skin, light freckles and a messy honey-blonde ponytail pushes a glossy marigold-amber wheelbarrow full of rolled turf across a freshly laid, vivid green lawn. She wears a fitted white tank, navy work overalls tied at the waist and sturdy boots, with "LazyTradie" printed on the side of the wheelbarrow. She's mid-stride and laughing, looking off to the side, totally in her element. Behind her is a clean, cloudless sky-blue sky and the edge of a navy timber fence. Hard bright sun, crisp shadows on the grass. Shot from a low angle so she stands tall against the sky. Full body. 4:5.

Shot on 35mm film, hard direct sun, crisp shadows, saturated colour, fine grain. Palette strictly deep navy (#0D1B2A), marigold amber (#F5A623), warm off-white and a touch of sky blue. Bold, playful, premium lifestyle advertising for an Australian trades brand. Models are young, radiant, styled like a fashion shoot. No food or drinks. No text except "LazyTradie" exactly as written.
```

**roofer**
```
A confident 26-year-old male model roofer with tousled sun-bleached hair and light stubble sits back on his heels on a pitched terracotta-tiled roof against a clean sky-blue sky. He wears a navy safety harness clipped to a roof anchor, an amber hi-vis vest with "LazyTradie" across the back, a white tee and navy work pants. One hand rests on a fresh row of tiles and he looks out over the suburb with a relaxed, satisfied smile, like the job's nearly done. The rope from his harness curves graphically across the tiles. Hard direct sun, crisp shadows of the tiles. Shot from a slightly higher angle on the roof, full body, with plenty of open sky above him. 4:5.

Shot on 35mm film, hard direct sun, crisp shadows, saturated colour, fine grain. Palette strictly deep navy (#0D1B2A), marigold amber (#F5A623), warm off-white and a touch of sky blue. Bold, playful, premium lifestyle advertising for an Australian trades brand. Models are young, radiant, styled like a fashion shoot. No food or drinks. No text except "LazyTradie" exactly as written.
```

---

## 4. What's real

Every claim maps to the product: the receptionist answers calls, SMS and web enquiries, checks live
free slots and books into the calendar; every booking shows in the dashboard's Jobs table and the
notification bell; tiers are the dashboard's own `T1 · Auto-book`, `T2 · Confirm`, `T3 · Emergency`.
The setup cards, sidebar and Jobs table are rendered from `lazytradie-backend` with the fictional
demo account (Turner Electrical, Melbourne). No "24/7" claim.
