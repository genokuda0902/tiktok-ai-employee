#!/usr/bin/env bash
set -euo pipefail
src="${1:?input MP4}"; out="${2:?output MP4}"
ffmpeg -hide_banner -loglevel error -y -i "$src" -map 0:v:0 -map 0:a:0 -c:v copy -af "volume=-0.7dB" -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$out"
