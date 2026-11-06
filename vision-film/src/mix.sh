#!/usr/bin/env bash
# Final mix: music (first 60 s, fade 57→60) ducked under the VO, + SFX, → −14 LUFS / −1.5 dBTP.  usage: mix.sh <dir with vo.wav sfx.wav> <out.wav>
set -e; D=$1; OUT=$2; M="$(dirname "$0")/../assets/music.mp3"
ffmpeg -loglevel error -y -i "$D/vo.wav" -i "$M" -i "$D/sfx.wav" -filter_complex "
[0]highpass=f=75,acompressor=threshold=-22dB:ratio=3:attack=6:release=160:makeup=2,equalizer=f=3200:t=q:w=1.2:g=2,aformat=channel_layouts=stereo,asplit=2[v][vsc];
[1]atrim=0:60,asetpts=PTS-STARTPTS,afade=t=out:st=57:d=3,volume=0.56[m];
[m][vsc]sidechaincompress=threshold=0.035:ratio=6:attack=20:release=420:makeup=1[md];
[2]volume=0.5[s];
[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 "$OUT"
