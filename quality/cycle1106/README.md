# cycle1106 — Before/After evidence ribbon + eight-cue signal QA

**REVIEW ONLY / NOT APPROVED FOR PUBLICATION.** New implementation, not the original v33 source. The input video and generated MP4 stay in private local conversation attachments, not GitHub. No automatic posting, merge, external media upload, paid contract or release approval.

## New vs cycle1104

The prior cycle repaired misleading transient totals in scene06. This cycle adds an explicit two-stage **BEFORE (total unverified) → AFTER (46+29=75 arithmetic verified)** comparison in the original 14.3–17.333s evidence scene, while preserving the underlying spreadsheet footage, existing numeric proof cards, all lower burned-in captions, and the identical AAC bitstream. It does **not** claim that data sources are correct, or that AI increased productivity. It responds to the user's reference 16-panel storyboard which has a Before/After beat; it is not a recreation of its human/robot cinematography.

A separate offline `audio_caption_audit.py` now measures PCM signal energy in **eight approximate visual scene windows**, including 20.3–23.033s. This is NOT independent ASR, VAD, a transcript, or proof of Japanese speech/caption semantic or temporal alignment. It is deliberately labeled as signal-only so future cycles do not mistake it for narration QA.

## Reproduce locally

Requires Python 3, Pillow, NumPy, FFmpeg/ffprobe, Noto Sans CJK, and the SHA-pinned **local review-only** cycle1104 MP4. The private source video is not included.

```bash
cd quality/cycle1106
python3 -m unittest -v test_before_after_evidence.py test_audio_caption_audit.py
python3 before_after_evidence.py \
  --source /PRIVATE/cycle1104_TRUTHFUL_PROOF_JP_REVIEW_ONLY.mp4 \
  --source-sha 074d169d08cb74778b314592d97a07cfd7b769574bbe64c0c08d9175a43c87f1 \
  --manifest manifest.json --out /PRIVATE/cycle1106_BEFORE_AFTER_PROOF_JP_REVIEW_ONLY.mp4 \
  --report /PRIVATE/qa1106.json
python3 audio_caption_audit.py --video /PRIVATE/cycle1106_BEFORE_AFTER_PROOF_JP_REVIEW_ONLY.mp4 --out /PRIVATE/audio_qa1106.json
```

## Verified local outcome (2026-11-01 JST)

- Input SHA256 `074d169d08cb74778b314592d97a07cfd7b769574bbe64c0c08d9175a43c87f1`.
- Output SHA256 `642b66140d2c115ea5c5c45c80b28a0d73612c7c0aad110f9c2a4119fcb3eedf`.
- H.264 1080x1920 30fps, 691 frames, 23.033333s; AAC 48kHz ADTS SHA unchanged `76801539a721f7d968b5a8bf725fd056ab00de5a74bd09caf50112993c4aa2f8`.
- 13 local unit tests PASS; full audio/video decode PASS; all 8 approximate audio windows have signal, **not** proof of speech content.
- 10 genre palettes and manifest validation tested; **only AI work** rendered as full MP4.
- Original reference storyboard directly inspected; original v33 MP4 not available for direct comparison this cycle. Past summaries of `TikTok市場分析` and `TikTok動画研究` consulted; complete original chat bodies not accessible.

## Release gates still blocked

Independent Japanese ASR and subtitle semantic/sync review, original v33 side-by-side, publication rights, employee approval, smartphone real playback, actual GitHub Actions charges. CI uses a generated **synthetic** 18s test input and does NOT validate the final local Japanese MP4. `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`.
