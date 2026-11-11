#!/usr/bin/env bash
set -euo pipefail
BASE="${1:?source MP4 required}"
OUT="${2:?output MP4 required}"
SRT="${3:?SRT path required}"
ffmpeg -hide_banner -loglevel error -y -i "$BASE" -vf "subtitles=${SRT}:force_style='FontName=Noto Sans CJK JP,FontSize=11,PrimaryColour=&H00FFFFFF,OutlineColour=&H00102228,BorderStyle=3,BackColour=&H990B1C22,Outline=1,Shadow=0,Alignment=2,MarginV=18'" -map 0:v:0 -map 0:a:0 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
