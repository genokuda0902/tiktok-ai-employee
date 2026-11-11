#!/usr/bin/env bash
set -euo pipefail
SRC="$1"
OUT="$2"
D=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$SRC")
START=$(python3 -c 'import sys;print(f"{float(sys.argv[1])-0.3:.3f}")' "$D")
ffmpeg -y -i "$SRC" -map 0:v:0 -map 0:a:0 -vf "fade=t=in:st=0:d=0.30,fade=t=out:st=$START:d=0.30" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
