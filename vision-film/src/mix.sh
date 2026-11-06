#!/usr/bin/env bash
# Final mix: the music edit (audio.py → music.wav) ducked under the VO, + SFX, faded over the last 4 s → −14 LUFS / −1.5 dBTP.
# usage: mix.sh <dir with vo.wav sfx.wav music.wav> <out.wav>
set -e; D=$1; OUT=$2
END=$(python3 -c "import json,os;print(json.load(open(os.path.join('$(dirname "$0")','timeline.json')))['dur'])")
FS=$(python3 -c "print($END-4)")
ffmpeg -loglevel error -y -i "$D/vo.wav" -i "$D/music.wav" -i "$D/sfx.wav" -filter_complex "
[0]highpass=f=75,acompressor=threshold=-22dB:ratio=3:attack=6:release=160:makeup=2,equalizer=f=3200:t=q:w=1.2:g=2,aformat=channel_layouts=stereo,asplit=2[v][vsc];
[1]afade=t=out:st=$FS:d=4,volume=0.56[m];
[m][vsc]sidechaincompress=threshold=0.035:ratio=5:attack=30:release=650:makeup=1[md];
[2]volume=0.45[s];
[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 "$OUT"
