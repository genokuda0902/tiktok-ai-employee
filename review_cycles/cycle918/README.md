# cycle918 — task-focus opening hook (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No TikTok posting, auto-merge, payment, private-media upload, or publication.

## Change vs cycle916 and parallel cycle917
The locally accessible cycle916 MP4 changed scene04 to an illustrated laptop prompt editor. Parallel open PR #297 (cycle917) changes scene07 to a reusable prompt template. This separate branch changes **scene01 only** (0–2.9s, 87 frames): three task cards → choose one → focus on one task. It is original vector artwork and introduces no claims about guaranteed time savings.

## Reproduce with your privately held source
Requirements: Python 3, Pillow, NumPy, FFmpeg, Noto Sans CJK fonts. Generate original frames:

    python3 review_cycles/cycle918/task_focus_hook.py --genre ai_work --out /private/cycle918_frames

Overlay on a privately held cycle916 MP4, keeping AAC bitstream and existing burned Japanese subtitles:

    ffmpeg -i /private/cycle916.mp4 -framerate 30 -start_number 0 -i /private/cycle918_frames/%03d.png -filter_complex "[0:v][1:v]overlay=x=0:y=300:eof_action=pass:enable='between(n,0,86)',format=yuv420p[v]" -map "[v]" -map 0:a:0 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r 30 -frames:v 691 -c:a copy -movflags +faststart /private/cycle918.mp4

The generated frame canvas is 1080×1160 and overlays y=300..1459, protecting inherited header and caption area. 10 genre copy/color presets are supported; only ai_work was made into a complete 23.033-second MP4.

## Local MP4 QA, not CI QA
Private finished MP4 SHA256: e073a85508eb4cf77d96339e673bb1784368cc12ae0619869117ddde875bc316.
Source MP4 SHA256: 47309852c5afbf0b4f7ed8238764d8a66a5c4412bd9007d4195d94907ba73c55.
AAC elementary ADTS SHA256 source/output: c2cf7807e183573d74fa7c3f1a719cfb05ccdcb0790ef8d28c2c902640bc197d.
H.264 1080×1920, 30fps, 691 frames, 23.033 seconds, AAC 48kHz.
All 691 video frames decoded; audio analyzed with FFmpeg. Local QA 18/18 passed. Scene01 87/87 frames changed; max outside-scene quarter-resolution mean absolute pixel difference 0.183; subtitle-band max 0.207. Audio loudness -16.61 LUFS, true peak -1.83 dBTP.

**GitHub CI only tests source renderer, 10-genre presets, safe area and synthetic frames. It does not receive or test the private MP4.**

## Sources and unresolved gates
Accessible summaries of TikTok市場分析 and TikTok動画研究 recommend strong opening hook, readable Japanese captions and purposeful visual cuts. Earlier cycle reports document direct inspection of the user's 16-panel ChatGPT×Excel storyboard. The original v33 MP4 was not accessible in this cycle. Independent Japanese ASR / subtitle timing, inherited source commercial rights, smartphone playback, employee approval and actual GitHub Actions billing remain unverified. Manual employee-approved posting only.
