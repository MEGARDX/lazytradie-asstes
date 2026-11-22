# Kinetic-type reel (22 Nov)
`lazytradie-kinetic-reel-9x16.mp4`: 16.0 s, 1080×1920, 30 fps, −14 LUFS.

A frame-matched remake of the owner's reference (`Uploads/19 Nov/Reel 11 nov/SaveClip.App_AQOVf….mp4`) for LazyTradie:
- one word per hit, with a hard cut that flips cream ↔ navy on every beat, speeding up toward the logo (the reference's exact cut times)
- the same effects in the same slots: blur-in, slide, scale-up, liquid warp, an amber dot dropping onto the "i", motion blur, the last word typing out, the logo warping away
- Outfit SemiBold (the reference's look), navy `#0E1E2F` and cream `#EFEBE1`, with brand amber in place of the reference's gold
- **Audio:** the reference's own track as one continuous build, with no restart in the middle. It plays up to its fast section, then that section (three hits about 0.29 s apart) loops six times, cut on the hits, before the track's own ending lands the logo. There's a soft tail under the end card.
- **One message, one logo** (owner, 22 Nov: no logo mid-video, no slowdown): "we don't just answer. we handle bookings, quotes, invoices, trust … results. and you, you don't just work. you get time back, weekends, footy, family … relax." → LazyTradie + "stress about work, not bookings." + comment "DEMO"

Rebuild: `cd src && python3 build_audio.py && node render.js && ./encode.sh` (build_audio.py also writes `cuts.js`, the cut times) (the first step needs `tmp/ref.wav`, which is ffmpeg'd from the reference).
Note: the track is the reference account's sound. If Instagram mutes it, post the video silent and add that sound in the app.
