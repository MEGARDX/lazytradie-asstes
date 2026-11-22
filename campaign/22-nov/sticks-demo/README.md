# "Stick explainer" format demo (22 Nov)
`lazytradie-sticks-demo-9x16.mp4`: a 10.2 s demo of the owner's reference format (`SaveClip.App_AQPnfLX….mp4`, a faceless cartoon presenter).

How the format works, and what the demo copies:
- **Presenter:** the character never animates. He hard-swaps between still pose drawings (point with a stick, shrug, finger up, hands out) on the sentence and the stressed word, with a hand-drawn "line boil" (the outlines jitter every 3 frames) so the stills feel alive.
- **Panel:** a sketch infographic on top, cut on every sentence, with a label pill, pastel fills, little burst marks, and a "VS" layout for comparisons.
- **Caption:** a black box with 2–3 words at a time; each word turns white as it's spoken.
- **Layout:** white background, the presenter in the bottom half, and a handle watermark at the bottom.
- **Demo content:** the LazyTradie tradie mascot (navy cap with a bolt badge, hi-vis vest, tool belt, work boots), all drawn in code as SVG. The VO is the owner's lines 01–05 with a quiet music bed.

For the full series, generate a pose sheet of the mascot (6–8 poses, same drawing) and one panel illustration per sentence in Gemini/Flow, then drop them in: `src/demo.html` swaps images the same way.
Rebuild: `cd src && python3 prep.py && node render.js && ffmpeg …` (see the commit for the encode line).
