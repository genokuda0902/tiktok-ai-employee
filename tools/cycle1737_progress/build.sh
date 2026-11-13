#!/usr/bin/env bash
set -euo pipefail
IN="${1:?input mp4}"; OUT="${2:?output mp4}"
D=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$IN")
ffmpeg -hide_banner -loglevel error -y -i "$IN" -f lavfi -i "color=c=0x55D7D2:s=1080x8:r=30" -filter_complex "[0:v]drawbox=x=0:y=75:w=iw:h=8:color=black@0.45:t=fill[bg];[bg][1:v]overlay=x='-W+W*min(t/${D},1)':y=75:shortest=1:format=auto,format=yuv420p[v]" -map '[v]' -map 0:a:0 -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a copy -movflags +faststart -t "$D" "$OUT"
