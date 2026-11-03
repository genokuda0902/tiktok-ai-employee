#!/usr/bin/env bash
set -euo pipefail
input="$1"; output="$2"
ffmpeg -hide_banner -loglevel error -y -i "$input" -map 0:v:0 -map 0:a:0 -c:v copy -af 'loudnorm=I=-16:TP=-1.5:LRA=11' -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$output"
