#!/usr/bin/env bash
set -euo pipefail
src="$1"; out="$2"
duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")
start=$(awk -v d="$duration" 'BEGIN{printf "%.3f",d-0.28}')
ffmpeg -hide_banner -loglevel error -y -i "$src" -map 0:v:0 -map 0:a:0 -c:v copy -af "afade=t=out:st=${start}:d=0.28" -c:a aac -b:a 192k -movflags +faststart "$out"
