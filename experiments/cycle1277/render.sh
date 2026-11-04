#!/usr/bin/env bash
set -euo pipefail
IN="${1:?input mp4}"; OUT="${2:?output mp4}"
ffmpeg -hide_banner -loglevel error -y -i "$IN" -f lavfi -i 'color=c=0x35D7CB:s=110x7:r=30' -filter_complex "[0:v]drawbox=x=36:y=1885:w=1008:h=7:color=white@0.20:t=fill[bg];[bg][1:v]overlay=x='36+(898)*min(t/22.23,1)':y=1885:shortest=1:format=auto,format=yuv420p[v]" -map '[v]' -map 0:a:0 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$OUT"
