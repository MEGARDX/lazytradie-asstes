# Kinetic-type reels (22 Nov), two parts
- `lazytradie-kinetic-part1-9x16.mp4`: "we don't just answer. we handle bookings, quotes, invoices, trust, speed, schedules, growth, cashflow, calendars, customers, job notes, results… lazy."
- `lazytradie-kinetic-part2-9x16.mp4`: "you don't just work. you get time back, weekends, footy, family, headspace, sleep, profit, holidays, your evenings, sanity, control… relax."

Each part is 12.4 s, 1080×1920, 30 fps, −14 LUFS, and is a frame-matched remake of the owner's reference (`Uploads/19 Nov/Reel 11 nov/SaveClip.App_AQOVf….mp4`):
- one word per hit, with a hard cut that flips cream ↔ navy on every beat, at the reference's exact cut times (they speed up into the logo at 8.9 s)
- the same effects in the same slots: blur-in, slide, scale-up, liquid warp, an amber dot dropping onto the "i", motion blur, and the last word typing out
- Outfit SemiBold, navy `#0E1E2F` and cream `#EFEBE1`, with brand amber in place of the reference's gold
- **The only logo is at the end** (owner, 22 Nov), held ~3.5 s: the LazyTradie wordmark on the hit, "stress about work, not bookings." on the next hit, then comment "DEMO" and lazytradie.com.au
- **Audio:** the reference's own track once, then a natural reverb tail of its last hits so the end card can hold

Rebuild: `cd src && python3 build_audio.py && V=1 node render.js tmp/p1 && V=2 node render.js tmp/p2 && ./encode.sh tmp/p1 lazytradie-kinetic-part1-9x16.mp4 && ./encode.sh tmp/p2 lazytradie-kinetic-part2-9x16.mp4`
(`tmp/ref.wav` is ffmpeg'd from the reference first.)
Note: the track is the reference account's sound. If Instagram mutes it, post the video silent and add that sound in the app.
