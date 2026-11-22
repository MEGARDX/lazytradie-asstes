# Kinetic-type reel (22 Nov)
`lazytradie-kinetic-reel-9x16.mp4`: 20.2 s, 1080×1920, 30 fps, −14 LUFS.

A frame-matched remake of the owner's reference (`Uploads/19 Nov/Reel 11 nov/SaveClip.App_AQOVf….mp4`) for LazyTradie:
- one word per hit, with a hard cut that flips cream ↔ navy on every beat, speeding up toward the logo (the reference's exact cut times)
- the same effects in the same slots: blur-in, slide, scale-up, liquid warp, an amber dot dropping onto the "i", motion blur, the last word typing out, the logo warping away
- Outfit SemiBold (the reference's look), navy `#0E1E2F` and cream `#EFEBE1`, with brand amber in place of the reference's gold
- **Audio:** the reference's own track, looped once (seamless join) to cover two passes, plus a soft tail under the end card
  - Pass 1: "we don't just answer. we handle bookings, quotes, invoices … lazy." → LazyTradie
  - Pass 2: "you don't just work. you get time back, weekends, footy, family … relax." → LazyTradie + "stress about work, not bookings." + comment "DEMO"

Rebuild: `cd src && python3 build_audio.py && node render.js && ./encode.sh` (the first step needs `tmp/ref.wav`, which is ffmpeg'd from the reference).
Note: the track is the reference account's sound. If Instagram mutes it, post the video silent and add that sound in the app.
