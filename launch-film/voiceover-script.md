# LazyTradie Launch Film: Every Line

Three kinds of voice. Only the first two are made in ElevenLabs.

**Pronunciation:** LazyTradie = LAY-zee TRAY-dee. In Veo prompts it's written as "Lazy Tradie" (two
words) so the model says it right.

---

## 1. Presenter, on camera: our narrator voice (Voice Changer or Chimera)

Generate the clip in Veo with these exact words (`LF_01`, `LF_02` in `footage-prompts.md`), then
convert the voice with **Voice Changer** using the same narrator voice as the explainer. Save as
`assets/vo/LF_01_vc.mp3` and `assets/vo/LF_02_vc.mp3`, and keep the untouched Veo MP4s.

| Clip | Line | Est. |
|---|---|---|
| `LF_01` ✓ made | You know the feeling. You're up a ladder, the phone's ringing, and that quote still isn't done. | 6.5 s |
| `LF_02` ✓ made | The tools got better. The admin didn't. … Until now. | 3.8 s |

### Presenter via Synthesia (one continuous take, replaces LF_01 + LF_02)

Synthesia has no 8-second limit, so the presenter can do the whole opening in one take, like the
reference. Paste this as a single scene (no extra scenes, titles, captions or music). ⏸ marks a
short pause; add it with Synthesia's pause marker, or just leave the punctuation to do it.

```
You know the feeling. You're up a ladder, the phone's ringing, and that quote you promised last week… still isn't done.
Every year, the tools get better. But the admin? It never did. ⏸
Until now.
```
About 13 s. Avatar: a man in a plain dark top on a plain white background, centred, 16:9, 1080p.
Voice: the narrator voice if your plan can import ElevenLabs voices (Enterprise). Otherwise pick a
deep, calm male English voice and I'll swap it to the narrator with Voice Changer; the lips stay in
sync because the timing doesn't change.

## 2. Narrator, off camera: text to speech (same narrator voice)

Same voice and settings as the explainer, so it carries straight on from the presenter.
One file per line, saved to `assets/vo/`.

| File | Line | Est. |
|---|---|---|
| `V_01` | Introducing LazyTradie. | 1.4 s |
| `V_02` | An AI receptionist that never misses a call, and a Copilot that handles the admin. So you can knock off on time. | 6.0 s |
| `V_03` | It answers every call, quotes the job, books it in… and chases what you're owed. | 4.6 s |
| `V_04` | And you stay in control of every quote, every booking, and every dollar. | 4.0 s |

```
Introducing LazyTradie.
```
```
An AI receptionist that never misses a call, and a Copilot that handles the admin. So you can knock off on time.
```
```
It answers every call, quotes the job, books it in… and chases what you're owed.
```
```
And you stay in control of every quote, every booking, and every dollar.
```

## 3. Characters: Veo's own voices (nothing to make in ElevenLabs)

These are spoken inside the Veo clips. Each prompt already asks for the accent and tone.

| Clip | Who | Line |
|---|---|---|
| `LF_03` ✓ made | Old tradie at his ute | About bloody time. |
| `LF_04` | His partner, backyard at golden hour | You're home early? |
| `LF_05` | Sparky chasing a car | Oi! You forgot to pay me! |
| `LF_06` | Partner at dinner (3D animated) | Wow. A whole dinner… and you haven't checked your phone once. |
| `LF_07` | Electrician (woman) at a switchboard | Try LazyTradie. |
| `LF_08` | Plumber under a sink | Try LazyTradie. |
| `LF_09` | Builder on site, points at the lens | Try LazyTradie. … Stress about work, not bookings. |

If a character comes out with the wrong accent or a flat read, regenerate it first. If the picture
is perfect but the voice isn't, run that clip through Voice Changer with a voice that suits the face.
