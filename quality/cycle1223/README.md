# Cycle 1223 — narration-reactive meter synchronization (REVIEW ONLY)

**Distinct improvement:** Cycle 1221 repaired the scene-3 spreadsheet evidence text. Cycle 1223 improves the **existing** seven-bar narration indicator: its amplitude and frequency bands now follow actual audio RMS/spectrum per 30-fps frame, with attack/release smoothing. No new speech, captions, background imagery, outside media, or publishing behavior is introduced. Ten configurable genre palettes are supported; only AI-work was rendered as a complete private MP4.

## Real video (conversation attachment only; not public GitHub)
Source: cycle1221, SHA256 e7217489d0754b6315a911b995e13d9c96befada391bcbd1fe6cdb615b7437d5.
Output: cycle1223, SHA256 d253f57d4af5cef5941e85915ed0a4bbc3fed118e61196d10ac0185a812e9680.
1080x1920, H.264, 30fps, 667 frames, 22.237s, eight chapters, AAC 48kHz Japanese tag. Full A/V decode PASS. AAC encoded ADTS SHA256 identical to source. Original burned subtitles and narration text were not intentionally altered. Protected region max sampled mean pixel difference 1.284/255. Correlation of video-meter bright pixels with voice amplitude, sampled every eight frames: 0.838 (before) -> 0.9206 (after). Correlation is a diagnostic, not an independent speech/transcription or perceived-quality score.

## Local and CI
Local unit tests 8/8 PASS; synthetic 2s/60-frame full A/V smoke PASS. CI runs those tests on **synthetic** media only. Real MP4, source screenshots, user reference media, and employee material must never be uploaded to this public repository. Run offline with FFmpeg, numpy and Pillow:
```bash
python quality/cycle1223/code/audio_reactive_meter.py --source /PRIVATE/previous.mp4 --output /PRIVATE/new.mp4 --workdir /PRIVATE/tmp --genre ai --report /PRIVATE/qa.json
```

## Sources and limitations
Accessible past summaries of TikTok市場分析/TikTok動画研究 and user's 16-panel ChatGPT×Excel時短術 storyboard were reviewed; original v33 MP4 was not accessible. The 16-panel cinematic reference remains far more diverse than this eight-scene slide video. Independent Japanese ASR, speech-caption semantic/timing audit, smartphone hardware playback, source asset rights, employee approval and actual Actions billing were **not verified**. Initial attempt generated 666 frames due to overlay shortest=1; corrected to shortest=0:eof_action=repeat. Two trial ROI positions were wrong and were corrected to x704,y1457,w150,h100 after pixel-coordinate inspection. No paid API, merge, public upload of real media or TikTok posting. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**
