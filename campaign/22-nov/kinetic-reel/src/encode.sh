#!/usr/bin/env bash
# frames + looped reference track → ../lazytradie-kinetic-reel-9x16.mp4 (-14 LUFS)
set -euo pipefail; cd "$(dirname "$0")"
ffmpeg -y -loglevel error -framerate 30 -i tmp/out/%05d.jpg -i tmp/audio.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart ../lazytradie-kinetic-reel-9x16.mp4
ls -l ../lazytradie-kinetic-reel-9x16.mp4
