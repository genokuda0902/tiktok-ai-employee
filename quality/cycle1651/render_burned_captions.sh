#!/usr/bin/env bash
set -euo pipefail
# Review-only reimplementation. Requires an approved/public-safe input video and SRT.
INPUT="${1:?input mp4 required}"
SRT="${2:?SRT required}"
OUT="${3:?output mp4 required}"
test -s "$INPUT"; test -s "$SRT"
ffmpeg -y -i "$INPUT" -vf "subtitles=$SRT:force_style='FontName=Noto Sans CJK JP,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00101010,BorderStyle=3,BackColour=&H99000000,MarginV=260,Alignment=2'" -map 0:v:0 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -movflags +faststart -an "$OUT"
# This deliberately emits no voice; never mark speech QA as passed.
ffmpeg -v error -i "$OUT" -f null -
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height -show_entries format=duration -of json "$OUT"
