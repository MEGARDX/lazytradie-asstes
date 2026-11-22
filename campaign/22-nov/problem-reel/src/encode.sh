#!/usr/bin/env bash
# Frames (tmp/out/%05d.jpg) + stereo mix (tmp/mix.wav) → final 9:16 MP4 under GitHub's 100 MB cap, loudness -14 LUFS.
set -euo pipefail
cd "$(dirname "$0")"
OUT=../lazytradie-problem-solution-reel-9x16.mp4
ffmpeg -y -loglevel error -framerate 30 -i tmp/out/%05d.jpg -i tmp/mix.wav \
  -map 0:v -map 1:a -c:v libx264 -preset slow -profile:v high -pix_fmt yuv420p -crf 19 -maxrate 14M -bufsize 28M \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart "$OUT"
ls -l "$OUT"
