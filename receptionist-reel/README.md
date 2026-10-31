# LazyTradie AI Receptionist Reel: Plan & Asset List (≈44 s)

A motion-graphics launch reel for the **AI Receptionist**, modelled beat for beat on the ElevenLabs
**"Introducing Vocals on Eleven Music"** reel
(`../SaveClip.App_AQNHIk458UOcVM-8WIgdltAADdKlL_09EDfgsWGiODGkIJNO0Rr-T7Zjds_sb0rc-OluXBtQV3Vol_l1DHnKknEf82sMHVP4TQGfoaM.mp4`).

- **Voiceover lines:** [`voiceover-script.md`](voiceover-script.md) → `assets/vo/`
- **Photos:** the 12 candid flash photos below → `assets/photos/`
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

### Montage: 12 new photos, candid flash style

The reference montage is candid direct-flash 35mm: real moments, not ads. So this set is different
from the campaign photos. Six pairs, swapping every ~0.4 s, each photo shown as a tall half-frame
strip, which is why they're 9:16 with the subject centred. The same photos feed the job cards in the
3D carousel. Save them to `assets/photos/` as `m01` … `m12`.

| Pair | Left | Right |
|---|---|---|
| 1 | `m01` sparky | `m02` plumber |
| 2 | `m03` crew | `m04` chippy |
| 3 | `m05` welder | `m06` tiler |
| 4 | `m07` sparky-board | `m08` high-five |
| 5 | `m09` painter | `m10` landscaper |
| 6 | `m11` roofer | `m12` knock-off |

**Style block** (already in each prompt):
> Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.

**m01 · sparky**
```
A young female electrician up a stepladder in a dark ceiling cavity at night, head torch on, wire strippers in her teeth, pulling a bundle of cables through a hole in the plasterboard, caught mid-laugh. The flash lights her and a cloud of dust.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m02 · plumber**
```
A young plumber lying on his back half inside a cramped under-sink cabinet, only his torso and legs out, wrench raised, water spraying from a pipe and catching the flash like glitter, his mate crouched beside him cracking up.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m03 · crew**
```
Five young tradies piled into the tray of a dusty ute at knock-off time on a building site at dusk, hi-vis vests open, one standing and pointing straight at the camera, the rest mid-laugh. Flash freezes the moment against a deep blue sky.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m04 · chippy**
```
A young carpenter in a navy tee ripping a sheet of plywood with a circular saw on a half-built timber frame at night. A fan of sawdust explodes off the blade and glows in the flash. Safety glasses, focused grin.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m05 · welder**
```
A young welder flipping his welding mask up mid-job in a dark steel workshop, face streaked with grime, a fountain of orange sparks still falling around him, caught in the flash.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m06 · tiler**
```
A young female tiler on her knees in a bare bathroom, grout on her hands and cheek, looking up at the camera over her shoulder with a cheeky grin, sleeves rolled up. Rows of fresh white tiles and spacers around her.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m07 · sparky-board**
```
A young electrician lit by his head torch and the flash at an open switchboard in a pitch-dark garage, multimeter probes in hand, sleeves rolled, deep concentration, his breath just visible in the cold.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m08 · high-five**
```
A young apprentice and her older boss in hi-vis high-fiving across a muddy job site at night under a single work light, both mid-shout, rain streaks frozen in the flash.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m09 · painter**
```
A young painter in paint-splattered white overalls on scaffolding outside a weatherboard house at dusk, roller raised overhead, amber paint drips flicking off it in the flash, looking down at the camera with a wide grin.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m10 · landscaper**
```
A young landscaper standing knee-deep in a muddy trench in the rain, shovel over one shoulder, soaked hi-vis, laughing up at the camera. The flash catches every raindrop.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m11 · roofer**
```
A young roofer crouched on a tin roof at blue hour, harness on, one hand raised in a fist to the sky in celebration of a finished job, flash lighting him against the dark suburb.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

**m12 · knock-off**
```
A young tradie crew dancing and celebrating in the shell of a nearly finished house at night under bare work lights, hard hats tossed in the air, hi-vis flying, pure joy, blurred motion in the flash.

Candid documentary photo, shot on 35mm film with a direct on-camera flash: harsh flash highlights, deep falling-off shadows, warm grainy colour, a touch of motion blur, a real unposed moment, gritty and alive, like a behind-the-scenes photo from a gig. Young Australian tradies full of character, natural, not models posing. Tall vertical frame, subject centred in the middle third. 9:16. No food or drinks. No text, no logos.
```

---

## 4. What's real

Every claim maps to the product: the receptionist answers calls, SMS and web enquiries, checks live
free slots and books into the calendar; every booking shows in the dashboard's Jobs table and the
notification bell; tiers are the dashboard's own `T1 · Auto-book`, `T2 · Confirm`, `T3 · Emergency`.
The setup cards, sidebar and Jobs table are rendered from `lazytradie-backend` with the fictional
demo account (Turner Electrical, Melbourne). No "24/7" claim.
