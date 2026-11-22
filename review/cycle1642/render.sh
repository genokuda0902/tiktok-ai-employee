#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-cycle1642_REVIEW_ONLY.mp4}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
bash "$(dirname "$0")/../cycle1641/render.sh" "$TMP/base.mp4" >/dev/null
# Nonverbal synthetic reference tone. This is NOT Japanese speech.
ffmpeg -hide_banner -loglevel error -y -i "$TMP/base.mp4" -f lavfi -i 'sine=frequency=440:sample_rate=48000:duration=20' -filter_complex '[1:a]volume=0.018,afade=t=in:st=0:d=0.4,afade=t=out:st=19:d=1[a]' -map 0:v:0 -map '[a]' -c:v copy -c:a aac -b:a 96k -shortest -movflags +faststart "$OUT"
ffmpeg -v error -i "$OUT" -f null -
python3 "$(dirname "$0")/verify.py" "$OUT"
