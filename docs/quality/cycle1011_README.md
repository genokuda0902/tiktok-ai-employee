# cycle1011 — silence-safe pacing (human review only)

## What changed from cycle1009
- cycle1009 removed duplicated selectable subtitles; the picture and audio timing were unchanged.
- cycle1011 removes four short, near-silent interior intervals while preserving >=300 ms of each pause, avoiding chapter boundaries, the first 600 ms and closing 330 ms.
- The original private AI-work review MP4 changed from 23.033333 s (691 frames) to 22.500000 s (675 frames). The removed 0.533333 s had RMS -61.9 to -64.6 dBFS.
- Eight chapter timestamps and the **external optional** SRT are retimed. There is no embedded duplicate subtitle.
- 10 genre IDs share one engine. Only AI-work was rendered with real content.

## Verified locally
- 1080x1920 H.264 30 fps, AAC 48 kHz Japanese language tag, 675 frames, eight chapters.
- Full audio/video decode PASS. Nine unit tests PASS. Synthetic 3-second integration PASS.
- Eight sampled scene frames matched original content (gray mean absolute difference 0.198-0.314 / 255, re-encode).
- Eight 0.25-second corresponding audio windows correlated at 1.0000 to 4 decimals; this is not independent Japanese transcription.
- All four removed audio spans were extremely quiet. This does not prove every Japanese syllable or caption alignment is correct.
- Finished private MP4 is **not** committed or uploaded to public GitHub. GitHub Actions uses synthetic 3-second audio/video only.

## Research, rights and limitations
Accessible prior TikTok research summaries emphasize the first 1.5 s hook, 15-25 s runtime, legible Japanese subtitles and approval-gated posting. User's 16-panel storyboard was discussed in prior work, but original v33 video is not available for direct comparison.

No independent Japanese ASR or phonetic/subtitle alignment, mobile-device playback, source rights verification, employee approval, reference-v33 parity, view-retention measurement or GitHub Actions billing verification. The video is **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid subscription, public video upload or automatic posting.

## Reproduce with an approved private source
```bash
python3 -m unittest discover -s tests -p 'test_cycle1011_silence_safe_trim.py' -v
python3 tools/quality/cycle1011_silence_safe_trim.py --source /private/input.mp4 --output /private/output.mp4 --srt /private/source.srt --genre ai_work
```
