# cycle899 — CTA action path / review only

## Difference from earlier cycles
cycle897: opening animation + 8-scene progress. cycle898: 5-bar narration-reactive visualizer. cycle899: **3-step CTA action path** in the final slide, 20.37–23.03s, emphasizing the existing check marks without covering subtitles.

## Provenance and local video
Rendered from locally available private **cycle897** MP4. The latest cycle898 private MP4 was unavailable in this run; no direct cycle898-to-899 media comparison is claimed. Finished video was verified locally: H.264 1080x1920, 30fps, 691 frames, 23.033s, AAC 48kHz mono; full A/V decode PASS; AAC ADTS SHA identical to source. 13 local technical checks PASS and 13 Python tests PASS. Caption-region sampled MAE max 1.231 (video re-encode noise).

The completed private MP4 and inherited imagery/voice are NOT in GitHub. CI validates only source, safe-zone rules, 10 genre identifiers and release gate, not the finished private MP4. Source-dependent positions are constants in cta_path.py; adapt only after human visual review.

## Local reproduction
Requires Python 3.11, Pillow, ffmpeg, source MP4.
1. python quality/cycle899/src/cta_path.py /tmp/c899
2. ffmpeg -i /private/source.mp4 -itsoffset 20.37 -framerate 30 -start_number 0 -i /tmp/c899/%04d.png -filter_complex '[0:v][1:v]overlay=0:0:format=auto:eof_action=pass:shortest=0,format=yuv420p[v]' -map '[v]' -map 0:a:0 -c:v libx264 -crf 17 -pix_fmt yuv420p -r 30 -c:a copy -frames:v 691 /private/review.mp4
3. python -m unittest discover -s quality/cycle899/tests -p 'test_*.py' -v

Original v33 reference MP4/full TikTok research chats, Japanese ASR/semantic subtitle match, inherited material commercial rights, smartphone playback, employee approval and actual Actions billing remain unverified. 10 genre code paths are checked; only 1 AI-productivity MP4 was rendered.

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid service, public media upload, or automatic posting.
